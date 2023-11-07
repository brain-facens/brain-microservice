# OCR Notas
<p align="center">
  <img src="docs/app_diagram.png">
</p>
Sistema para processamento de texto em notas fiscais, com o objetivo de realizar a identificação de campos relevantes em uma nota e otimizar sistemas de boneficação ou validação. Facilidando a vida de logistas, comerciantes e gestores, a aplicação conta com uma interface que captura imagens da webcam, realiza o processamento da imagem por meio de OCR e disponibiliza a visualização dos resultados obtidos.

## Primeiros passos

Este projeto foi desenvolvido para executar uma interface web, onde o usuário terá acesso ao sistema de captura de imagens e os dados processados desta mesma imagem. Siga os passos a seguir para utilizar este projeto, a versão estável está na branch master.

### Prerequisitos

Para o bom funcionamento, é ideal que os requsitos abaixo sejam atendidos:

- Ubuntu 20.04 (Ambiente de desenvolvimento original, mas é compatível com 18.04 e 22.04)
- Docker Engine ou Docker Desktop
- Python 3.8
- Git
- Anaconda/Miniconda
- Desejáveis
  - CUDA 10.1 / CUDA 10.2
  - cuDNN 7.6
- Crie um ambiente virtual para o projeto caso queira trabalhar sem virtualização;
 
  ```
  conda create --name paddle_env python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

  # Ative o ambiente
  conda activate paddle_env
  ```

---
**Atenção!**
**Recomendamos que utilize o container Docker desenvolvido para este projeto, pois a aplicação é estável. Evitando assim, o risco de instalações erradas, erros de paths e versões de bibliotecas.**

---

### Instalação 

Localmente:

```
# Ative o ambiente
conda activate paddle_env

git clone https://github.com/brain-facens/OCR-notas.git

cd OCR-notas
pip install -r requirements.txt
```

Docker:
```
# Download da imagem do projeto
docker push natavitorino/ocr_paddle:1.2

```


## Utilização

Localmente:

```
streamlit run interface.py
```

Docker:
```
# Execução do conteiner com a aplicação
docker run -it --rm --name OCR --privileged --net=host --env=NVIDIA_VISIBLE_DEVICES=all --env=NVIDIA_DRIVER_CAPABILITIES=all --env=DISPLAY --env=QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix natavitorino/ocr_paddle:1.2 bash
```
---
**Atenção!**
A execução do container iniciará a interface e gerará a url (localhost:8004), ela dará acesso a interface.

---

## Demonstração

<p align="center">
  <img src="img/demo_image.png">
</p>

---

## 🤝 Collaborators

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/64169072?v=4" width="100px;" alt="Foto do Natanael Vitorino no GitHub"/><br>
        <sub>
          <b>Natanael Vitorino</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/98903288?v=4" width="100px;" alt="Foto do Pedro Gabriel no GitHub"/><br>
        <sub>
          <b>Pedro Gabriel</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## 📝 License

This project is under license. See the file [LICENSE](LICENSE) for more details.

---
