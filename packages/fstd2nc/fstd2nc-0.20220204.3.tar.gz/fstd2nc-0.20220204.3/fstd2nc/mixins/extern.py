###############################################################################
# Copyright 2017-2021 - Climate Research Division
#                       Environment and Climate Change Canada
#
# This file is part of the "fstd2nc" package.
#
# "fstd2nc" is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# "fstd2nc" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with "fstd2nc".  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

from fstd2nc.stdout import _, info, warn, error
from fstd2nc.mixins import BufferBase
import collections

#################################################
# Provide various external array interfaces for the FSTD data.

# Method for reading a block from a file.
def _read_block (filename, offset, length):
  import numpy as np
  with open(filename,'rb') as f:
    f.seek (offset,0)
    return np.fromfile(f,'B',length)

# Method for selecting a subset of data from a block of data.
def _subset (block, start, end):
  return block[start:end]

# Method for merging arrays together.
def _concat (*data):
  import numpy as np
  return np.concatenate(data)


class ExternOutput (BufferBase):

  # Helper method to get graph for raw input data.
  def _graphs (self):
    from fstd2nc.extra import blocksize
    from os.path import getsize
    import numpy as np
    graphs = [None] * self._nrecs
    ###
    # Special case: already have a dask object from external source.
    # (E.g., from fstpy)
    if hasattr(self, '_extern_table'):
      for rec_id in range(self._nrecs):
        d = self._extern_table['d'].iloc[rec_id]
        if hasattr(d,'compute'):
          # Start a dask graph using the external dask array as the source.
          graph = (d.compute,)
          graph = (np.ravel, graph, 'K')
        else:  # Special case: have a numpy array in memory.
          graph = d
          graph = np.ravel(graph, 'K')
        graphs[rec_id] = {None:graph}
      return graphs
    ###
    # Otherwise, construct graphs with our own dask wrapper.
    blocksizes = dict()
    fs_blocks = dict()
    all_file_ids = np.array(self._headers['file_id'],copy=True)
    all_swa = np.array(self._headers['swa'],copy=True)
    all_lng = np.array(self._headers['lng'],copy=True)
    for rec_id in range(self._nrecs):
      graph = dict()
      file_id = all_file_ids[rec_id]
      filename = self._files[file_id]
      if filename not in blocksizes:
        blocksizes[filename] = max(blocksize(filename), 2**20)
      bs = blocksizes[filename]
      offset = all_swa[rec_id] * 8 - 8
      length = all_lng[rec_id] * 4
      current_block = offset // bs
      pieces = []
      while current_block * bs < offset + length:
        s1 = max(current_block*bs, offset) - current_block*bs
        s2 = min(current_block*bs+bs, offset+length) - current_block*bs
        if (filename,current_block) not in fs_blocks:
          fs_blocks[(filename,current_block)] = (_read_block, filename, current_block*bs, bs)
        graph[filename+'-block-'+str(current_block)] = fs_blocks[(filename,current_block)]
        pieces.append( (_subset, filename+'-block-'+str(current_block), s1, s2) )
        current_block = current_block + 1
      if len(pieces) > 1:
        graph[filename+'-raw-'+str(offset)] = (_concat,) + tuple(pieces)
      else:
        graph[filename+'-raw-'+str(offset)] = pieces[0]
      graph[filename+'-decode-'+str(offset)] = (np.transpose, (self._decode, filename+'-raw-'+str(offset)))
      graph[None] = filename+'-decode-'+str(offset)
      graphs[rec_id] = graph
    return graphs

  def _iter_dask (self):
    """
    Iterate over all the variables, and convert to dask arrays.
    """
    from fstd2nc.mixins import _iter_type, _chunk_type, _var_type
    from dask import array as da
    from dask.base import tokenize
    import numpy as np
    from itertools import product
    from dask import delayed
    from fstd2nc.extra import decode
    unique_token = tokenize(self._files,id(self))
    graphs = self._graphs()
    self._makevars()
    for var in self._iter_objects():
      if not isinstance(var,(_iter_type,_chunk_type)):
        yield var
        continue
      name = var.name+"-"+unique_token
      ndim = len(var.axes)
      shape = var.shape
      # Convert _iter_type to more generic _chunk_type.
      if isinstance(var,_iter_type):
        chunks = {}
        ndim_outer = var.record_id.ndim
        ndim_inner = ndim - ndim_outer
        chunk_shape = shape[ndim_outer:]
        for ind in product(*map(range,var.record_id.shape)):
          rec_id = var.record_id[ind]
          ind = ind + tuple((0,dx) for dx in shape[ndim_outer:])
          chunks[ind] = rec_id
        var = _chunk_type (var.name, var.atts, var.axes, var.dtype, chunks, chunk_shape)
      # Convert _chunk_type to dask Array objects.
      if isinstance(var,_chunk_type):
        ndim_inner = len(var.chunksize)
        ndim_outer = ndim - ndim_inner
        # Get chunk dimensions.
        # First, size of single (untruncated) chunk, full indices.
        untruncated_chunksize = (1,)*(ndim-len(var.chunksize)) + var.chunksize
        # Next, breakdown of chunks along all variable dimensions.
        chunks = []
        chunk_indices = []
        for i in range(ndim):
          dx = untruncated_chunksize[i]
          ch = tuple(dx for j in range(dx,shape[i]+1,dx))
          if shape[i] % dx > 0:
            ch = ch + (shape[i] % dx, )
          chunks.append(ch)
          chunk_indices.append(range(len(ch)))
        # Loop over all indices, generate dask graph.
        dsk = dict()
        for ind, chunk_shape in zip(product(*chunk_indices), product(*chunks)):
          # Unique key for this graph member.
          key = (name,) + ind
          # Get record id.
          slices = [(i*dx,i*dx+res) for i,dx,res in zip(ind,untruncated_chunksize,chunk_shape)]
          slices[:ndim_outer] = ind[:ndim_outer]
          rec_id = var.chunks.get(tuple(slices),-1)
          # Add this record as a chunk in the dask Array.
          # Also, specify the preferred order of reading the chunks within the
          # file.
          if rec_id >= 0:
            graph = graphs[rec_id][None]
            dsk.update(graphs[rec_id])
            del dsk[None]
            dsk[key] = (np.reshape, graph, chunk_shape)
          else:
            # Fill missing chunks with fill value or NaN.
            if hasattr(self,'_fill_value'):
              var.atts['_FillValue'] = self._fill_value
              dsk[key] = (np.full, chunk_shape, self._fill_value, var.dtype)
            else:
              dsk[key] = (np.full, chunk_shape, float('nan'), var.dtype)
        array = da.Array(dsk, name, chunks, var.dtype)
        var = _var_type(var.name,var.atts,var.axes,array)
      yield var

  def to_xarray (self):
    """
    Create an xarray interface for the RPN data.
    Requires the xarray and dask packages.
    """
    from collections import OrderedDict
    import xarray as xr
    out = OrderedDict()
    for var in self._iter_dask():
      if not hasattr(var,'array'): continue
      out[var.name] = xr.DataArray(data=var.array, dims=var.dims, name=var.name, attrs=var.atts)
      # Preserve chunking information for writing to netCDF4.
      if hasattr(var.array,'chunks'):
        chunk_shape = [c[0] for c in var.array.chunks]
        out[var.name].encoding['chunksizes'] = chunk_shape
        out[var.name].encoding['original_shape'] = out[var.name].shape

    # Construct the Dataset from all the variables.
    out = xr.Dataset(out)
    # Decode CF metadata
    out = xr.conventions.decode_cf(out)

    # Make the time dimension unlimited when writing to netCDF.
    out.encoding['unlimited_dims'] = ('time',)

    return out

  def to_iris (self):
    """
    Create an iris interface for the RPN data.
    Requires iris >= 2.0, xarray >= 0.10.3, and dask.
    Returns a CubeList object.
    """
    from iris.cube import CubeList
    out = []
    for var in self.to_xarray().data_vars.values():
      # Omit some problematic variables.
      if var.dtype == '|S1': continue
      # Need to clean up some unrecognized metadata.
      for coord in var.coords.values():
        # Remove units of 'level' (confuses cf_units).
        if coord.attrs.get('units',None) in ('level','sigma_level'):
          coord.attrs.pop('units')
        # Remove non-standard standard names.
        if coord.attrs.get('standard_name',None) == 'atmosphere_hybrid_sigma_ln_pressure_coordinate':
          coord.attrs.pop('standard_name')
      out.append(var.to_iris())
    return CubeList(out)

  def to_pygeode (self):
    """
    Create a pygeode interface for the RPN data.
    Requires pygeode >= 1.2.0, and xarray/dask.
    """
    _fix_to_pygeode()
    from pygeode.ext_xarray import from_xarray
    data = self.to_xarray()
    return from_xarray(data)

  def to_fstpy (self):
    """
    Create a table compatible with the fstpy module.
    Requires pandas and dask.
    """
    import pandas as pd
    import numpy as np
    from fstpy.dataframe import add_grid_column
    from fstpy.std_io import add_dask_column
    # Special case: our data is already from an fstpy table, not from an FSTD
    # file in our control.
    # E.g., if some smartass does Buffer.from_fstpy(df).to_fstpy()
    if hasattr(self, '_extern_table'):
      return self._extern_table
    # Put all the header info into a dictionary.
    fields = ['nomvar', 'typvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4', 'datev']
    table = dict()
    # Create a mask to exclude deleted / overwritten records.
    mask = self._headers['dltf'] == 0
    for field in fields:
      col = self._headers[field][mask]
      # Convert byte arrays to strings, which is what fstpy expects.
      if col.dtype.str.startswith('|S'):
        col = np.asarray(col,dtype=col.dtype.str.replace('|S','<U'))
      table[field] = col
    # Convert to pandas table.
    table = pd.DataFrame.from_dict(table)
    # Add grid info.
    add_grid_column (table)
    # Temporarily insert some extra columns needed for the data.
    table['shape'] = list(zip(table['ni'],table['nj']))
    filenames = dict((i,f) for i,f in enumerate(self._files))
    table['path'] = pd.Series(self._headers['file_id'][mask]).map(filenames)
    table['key'] = (self._headers['key'][mask] << 10)
    # Generate dask objects
    #TODO: use our own, in case we modified the data?
    # (doesn't normally happen, but you never know...)
    # For instance could happen if interp is used.
    add_dask_column(table)
    # Clean up temporary columns and return.
    table.drop(columns=['shape','path','key'], inplace=True)
    return table

# Workaround for recent xarray (>0.10.0) which changed the methods in the
# conventions module.
# Fixes an AttributeError when using to_pygeode().
def _fix_to_pygeode (fixed=[False]):
  if fixed[0] is True: return
  try:
    from xarray.coding import times
    from xarray import conventions
    if not hasattr(conventions,'maybe_encode_datetime'):
      conventions.maybe_encode_datetime = times.CFDatetimeCoder().encode
    if not hasattr(conventions,'maybe_encode_timedelta'):
      conventions.maybe_encode_timedelta = times.CFTimedeltaCoder().encode
  except (ImportError,AttributeError):
    pass
  fixed[0] = True

class ExternInput (BufferBase):
  @classmethod
  def from_fstpy (cls, table, **kwargs):
    import tempfile
    from os import path
    import rpnpy.librmn.all as rmn
    import numpy as np
    if hasattr(table,'to_pandas'):
      table = table.to_pandas()
    # Construct the record header info from the table.
    fields = ['nomvar', 'typvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4', 'datev']
    headers = {}
    for col in fields:
      headers[col] = table[col].values.copy()
    # Pad out string variables with spaces.
    headers['nomvar'] = np.asarray(headers['nomvar'], dtype='|S4')
    headers['typvar'] = np.asarray(headers['nomvar'], dtype='|S2')
    headers['etiket'] = np.asarray(headers['etiket'], dtype='|S12')
    headers['grtyp'] = np.asarray(headers['grtyp'], dtype='|S1')
    headers['nomvar'] = np.char.ljust(headers['nomvar'], 4, ' ')
    headers['typvar'] = np.char.ljust(headers['typvar'], 2, ' ')
    headers['etiket'] = np.char.ljust(headers['etiket'], 12, ' ')
    # Add other fields that may be needed.
    if 'dltf' not in headers:
      headers['dltf'] = np.zeros(len(headers['nomvar']), dtype='int32')
    # Generate temporary file with target grid info.
    try: # Python 3
      grid_tmpdir = tempfile.TemporaryDirectory()
      gridfile = path.join(grid_tmpdir.name,"grid.fst")
    except AttributeError: # Python 2 (no auto cleanup)
      grid_tmpdir = tempfile.mkdtemp()
      gridfile = path.join(grid_tmpdir,"grid.fst")
    # Write all grid records to a temporary file, so they are accessible to
    # the vgrid / librmn helper functions.
    iun = rmn.fstopenall(gridfile, rmn.FST_RW)
    for nomvar in (b'!!  ',b'>>  ',b'^^  ',b'^>  ',b'!!SF'):
      for ind in np.where(headers['nomvar'] == nomvar)[0]:
        rec = table.iloc[ind].to_dict()
        rec['d'] = np.asarray(rec['d'])
        rmn.fstecr(iun, rec)
    rmn.fstcloseall(iun)

    # Initialize the Buffer object with this info.
    b = cls(gridfile, _headers=headers, **kwargs)
    b._grid_tmpdir = grid_tmpdir  # Save tmpdir until cleanup.

    # Save the dataframe for reference.
    # Will need the dask objects for getting the data.
    b._extern_table = table

    return b

  # Handle external data sources.
  # Overrides the usual reading of data from a file.
  def _fstluk (self, rec_id, dtype=None, rank=None, dataArray=None):
    import numpy as np
    # Check if there is custom data enabled for this Buffer.
    if hasattr(self, '_extern_table'):
      # Make sure we are looking for something in our list of records.
      # (could be a key pointing into something else?)
      if not isinstance(rec_id,dict):
        # Extract the record info from the table.
        rec = self._extern_table.iloc[rec_id].to_dict()
        # Load the data (if delayed).
        rec['d'] = np.asarray(rec['d'])
        return rec
    # Otherwise, continue as usual.
    return super(ExternInput,self)._fstluk (rec_id, dtype, rank, dataArray)

