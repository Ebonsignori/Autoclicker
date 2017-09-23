# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['.\\img:.\\sounds', 'C:\\Users\\Evan\\OneDrive\\Projects\\Python\\Autoclicker'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Auto[Click]Mate',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='img\\icon.ico')
