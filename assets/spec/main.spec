# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py', 'settings.py', 'presence.py', 'lunaroplayers.py', 'imrec.py'],
    pathex=[],
    binaries=[],
    datas=[('lunaroplayers.db','.'), ('lib/discord_game_sdk.bundle', '.'), ('lib/discord_game_sdk.dll', '.'), ('lib/discord_game_sdk.dll.lib', '.'), ('lib/discord_game_sdk.dylib', '.'), ('lib/discord_game_sdk.so', '.'), ('lib', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='icon.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    one_file=True
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
