# ginza_srclib

https://megagonlabs.github.io/ginza/

## Install

### 1. GiNZA + 従来型モデル の場合
Anaconda Powershell Prompt で、
pip install -U ginza ja_ginza
こちらを使うほうが、他のソフトウェアが使用するTransformersとの要求バージョンの相違の問題が発生しない。

### 2. GiNZA + Transformersモデル の場合
（Transformersモデルの実行には16GB以上のメモリ容量が必要。
メモリ容量が不足する場合は後述の従来型モデルを使用。」）
Anaconda Prompt か Anaconda Powershell Prompt で、
pip install -U ginza ja_ginza_electra

### エラー対応  

  ModuleNotFoundError: No module named 'sentencepiece' が表示された場合は、
  Anaconda Powershell Prompt で以下を実行。

  pip install sentencepiece

以上