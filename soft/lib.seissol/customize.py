#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

##############################################################################
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    fp=i['full_path']

    ver=''

    p0=os.path.basename(fp)
    p1=os.path.dirname(fp)
    print(p0,p1)

    lst=os.listdir(p1)
    for fn in lst:
        if fn.startswith(p0):
           x=fn[len(p0):]
           if x.startswith('.'):
              ver=x[1:]
              break

    return {'return':0, 'cmd':'', 'version':ver}

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)
    p3=os.path.dirname(p2)

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    hplat=hosd.get('ck_name','')

    ttags=tosd.get('tags',[])

    win=tosd.get('windows_base','')
    mingw=tosd.get('mingw','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    ep=cus['env_prefix']

    # Processing directories
    p1=os.path.dirname(fp) # installation directory
    p2=os.path.dirname(p1) # top dir with src

    env[ep]=p2

    px=os.path.join(p1,'include')
    if os.path.isdir(px):
       cus['path_include']=px

    pl=os.path.join(p1,'lib')
    if os.path.isdir(pl):
       cus['path_lib']=pl

       r = ck.access({'action': 'lib_path_export_script', 
                      'module_uoa': 'os', 
                      'host_os_dict': hosd, 
                      'lib_path': cus.get('path_lib','')})
       if r['return']>0: return r
       s += r['script']

    pb=os.path.join(p1,'bin')
    if os.path.isdir(pb):
       cus['path_bin']=pb

    # Check Maple path
    ps=os.path.join(p2, 'src')
    if os.path.isdir(ps):
       env[ep+'_SRC']=ps

       maple_path=os.path.join(ps, 'Maple')
       if os.path.isdir(maple_path):
          env[ep+'_MAPLE']=maple_path

    # Check binary
    fbin=''
    for f in os.listdir(pb):
        f1=os.path.join(pb,f)
        if os.path.isfile(f1) and f.startswith('SeisSol_'):
           fbin=f
           break

    if fbin=='':
       return {'return':1, 'error':'SeisSol binaries were not found'}

    env[ep+'_BINARY']=fbin
    env[ep+'_BINARY_FULL']=os.path.join(pb,fbin)

    return {'return':0, 'bat':s}
