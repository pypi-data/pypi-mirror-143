# 配布物のビルド
`python setup.py sdist`

# wheelパッケージのビルド
`python setup.py bdist_wheel`

# パッケージのアップロード
twine upload dist/*

コマンド実行後、ユーザー名・パスワードを入力。

# PyPI API Tokenの発行
- PyPI > Account Settings
- API tokens > Add API tokenをクリック

# GitHub Actions用の認証情報登録
- GitHubの対象リポジトリ > Settings > Secrets > Actions
- New repository secretを押下し、以下の情報を入力
    - Name: PYPI_API_TOKEN
    - Value: PyPIで発行したAPI Token