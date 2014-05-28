# coding: utf-8

def galapagos_to_pandas(in_filename='/home/ppzsb1/quickdata/GAMA_9_all_combined_gama_only_bd6.fits',
                        out_filename=None):
    """Convert a GALAPAGOS multi-band catalogue to a pandas-compatible HDF5 file"""
    from astropy.io import fits
    import pandas as pd
    import re
    import tempfile
    
    if out_filename is None:
        out_filename = re.sub('.fits$', '', in_filename)+'.h5'
    data = fits.getdata(in_filename, 1)
    with tempfile.NamedTemporaryFile() as tmp:
        with pd.get_store(tmp.name, mode='w') as tmpstore:
            for n in data.names:
                d = data[n]
                if len(d.shape) == 1:
                    new_cols = pd.DataFrame(d, columns=[n])
                else:
                    new_cols = pd.DataFrame(d, columns=['{}_{}'.format(n,b) for b in 'RUGIZYJHK'])
                tmpstore[n] = new_cols
            with pd.get_store(out_filename, mode='w', complib='blosc', complevel=5) as store:
                # Use format='table' on next line to save as a pytables table 
                store.put('data', pd.concat([tmpstore[n] for n in data.names], axis=1))
    return pd.HDFStore(out_filename)
