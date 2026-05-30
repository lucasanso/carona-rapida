# Carona Rápida

O Carona Rápida é uma plataforma ponta a ponta desenvolvida para a gestão de caronas. O projeto combina um ecossistema robusto de microsserviços containerizados, uma API de alta disponibilidade e uma interface simples focada na praticidade e experiência do usuário.

---

## Arquitetura e tecnologias

A aplicação foi desenhada seguindo os princípios de infraestrutura escalável, isolamento de rede e segurança de borda:

* Frontend UI: [Streamlit](https://streamlit.io/) — Interface fluida, responsiva e integrada para a interação do usuário.
* Backend API: [FastAPI](https://fastapi.tiangolo.com/) — REST API assíncrona para o processamento do CRUD e regras de negócio.
* Banco de Dados: [PostgreSQL](https://www.postgresql.org/) — Camada de persistência relacional.
* Gerenciamento de Dados: [pgAdmin4](https://www.pgadmin.org/) — Interface web para administração e monitoramento do banco de dados.
* Proxy Reverso: [Nginx Proxy Manager](https://nginxproxymanager.com/) — Roteamento de domínios e gerenciamento de tráfego interno.
* Segurança e Borda: [Cloudflare Tunnel (`cloudflared`)](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) — Túnel encriptado de dentro para fora, garantindo conectividade segura, TLS de borda e anulando a necessidade de exposição de portas residenciais.

### Detalhes de segurança

* Criptografia de senhas: As senhas dos usuários, ao serem cadastrados, são criptografadas.
* Username invés de Email: A abordagem de utilizar somente username e senha do usuário no login é para evitar que, caso ocorra alguma vulnerabilidade no banco, os dados sensíveis dos usuários não sejam comprometidos.

---
## Como acessar
A plataforma está publicada e disponível publicamente através do endereço oficial protegido e com certificado da Cloudflare:

**[https://caronarapida.com.br](https://caronarapida.com.br)**


