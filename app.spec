# -*- mode: python ; coding: utf-8 -*-
import os
import stat

a = Analysis(
    [os.path.join('src', 'app.py')],
    pathex=[],
    binaries=[],
    datas=[(os.path.join('src', 'assets'), 'assets'), ('obs', 'obs')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='tracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Set execute permissions on the generated executable
if hasattr(exe, 'name'):
    exe_path = os.path.join(DISTPATH, exe.name)
    if os.path.exists(exe_path):
        current_permissions = os.stat(exe_path).st_mode
        os.chmod(exe_path, current_permissions | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
