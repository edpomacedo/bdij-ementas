# bdij-ementas

![doi:10.5281/zenodo.10329194](https://zenodo.org/badge/DOI/10.5281/zenodo.10329194.svg)

Automação de rotina de publicação de ementas na Base de Dados de Institutos Jurídicos.

## Estrutura

- `/payload`: Diretório dividido em subdiretórios, sendo cada subdiretório uma fonte de ementas e cada arquivo `.txt` uma ementa a ser publicada.

## Pré-requisitos

Utiliza credenciais [OAuth](https://web.bdij.com.br/wiki/Special:OAuthListConsumers) da Base de Dados de Institutos Jurídicos e as bibliotecas `requests` e `requests_oauthlib`.

```bash
pip install -r requirements.txt
```

## Instalação

```bash
git clone https://github.com/edpomacedo/bdij-ementas.git
cd bdij-ementas
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

1. Selecione uma fonte autêntica de jurisprudência.
2. Crie um subdiretório dentro de `./payload/`.
3. Crie um `arquivo.txt` segundo as diretrizes abaixo.
4. A primeira linha do `arquivo.txt` será o título da página, obedecendo a classe processual e a numeração única do CNJ, p.ex. `ApCiv`:`0000000-00.0000.0.00.0000`.
5. A segunda linha em diante do `arquivo.txt` será o conteúdo da ementa.
6. Execute o comando `python main.py`.
7. Informe o nome do subdiretório criado e pressione `enter`.

Havendo uma página com identidade de título, a edição/criação da página não será realizada.

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para a sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -am 'Adicione uma nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um novo Pull Request

## Licença

Copyright 2023 EDPO AUGUSTO FERREIRA MACEDO

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contato

[Base de Dados de Institutos Jurídicos](https://github.com/bdij)