develop : ![develop](https://github.com/HelloAsso/HaApiV5/actions/workflows/test_pipeline.yml/badge.svg?branch=develop)  |  main : ![develop](https://github.com/HelloAsso/HaApiV5/actions/workflows/test_pipeline.yml/badge.svg?branch=main)

Bibliothèque python facilitant l'usage de l'api Helloasso. Compatible de python3.6 jusqu'à python 3.10

## INSTALLATION


pip install helloasso-apiv5


## USAGE

```python
api = HaApiV5(
        api_base='api.helloasso.com',
        client_id=XXXXXX,
        client_secret=XXXXXX,
        timeout=60
    )
```
|paramètres  											|  info | type |
| ----------------------------------------------------- |:-------------:| -----:|
|	api_base											|	url de l’api , exemple: api.helloasso.com	|	str	|
|	client_id											|	client_id pour l’authentification				|	str	|
|	client_secret										|	client_secret pour l’authentification			|	str	|
|	timeout(OPTIONAL)									|	Combien de temps faut-il attendre pour que le serveur envoie les données avant d'abandonner	|	float or int	|
|	access_token (OPTIONAL)								|	Le jeton d'accès OAuth s'il existe	|	str	|
|	oauth2_token_getter (OPTIONAL)	                    |	Vous pouvez utiliser les kwargs oauth2_token_getter et oauth2_token_setter sur le client pour utiliser un stockage personnalisé (partage entre instance / switch de tokens).	|	function	|
|	oauth2_token_setter (OPTIONAL)	                    |	Vous pouvez utiliser les kwargs oauth2_token_getter et oauth2_token_setter sur le client pour utiliser un stockage personnalisé (partage entre instance / switch de tokens).	|	function	|



## AUTHENTIFICATION


La documentation complète est disponible ici : https://api.helloasso.com/v5/swagger/ui/index

L'authentification est gérée par le SDK, Il suffit de fournir client_id et client_secret lors de 
l'instanciation de la classe HaApiV5. Le SDK se charge de gérer les appels pour obtenir des 
access et refresh tokens ainsi que les éventuels rafraichissements.


## AUTHORIZATION


Pour obtenir des droits sur des ressources protégées il est nécessaire de passer par la mire d'authorisation.

La methode generate_authorize_request génère l'url permettant de récupérer le consentement utilisateur

```python
from apiv5 import ApiV5

api = ApiV5(
        api_base='api.helloasso.com',
        client_id=XXXXXX,
        client_secret=XXXXXX,
        timeout=60
    )

request = api.authorization.generate_authorize_request(redirect_url="https://url.de.callback/callback", state="123")
full_url = request["full_url"]
code_verifier = request["code_verifier"]
```

Gardez le code_verifier, il permettra plus tard de finaliser le processus d'autorisation.

Dirigez l'utilisateur vers l'url présente dans full_url, il lui sera demandé de valider l'autorisation.
Un callback sera alors effectué vers la redirect_url renseignée.

Ce callback contient notamment le code nécessaire à la prochaine étape, récupérez ce code et appelez la methode suivante :

```python
response = api.authorization.exchange_authorization_token(authorization_code, "https://url.de.callback/callback", code_verifier)
```

exchange_authorization_token renvoie l'access_token permettant d'accèder aux données de l'association. (Voir méthode)

```python
api.set_access_token(response["access_token"])
response = api.call("/v5/users/me/organizations")
```

Pour plus de détails sur la procédure d'autorisation : https://drive.google.com/file/d/1SmzEDQsiPX6h97otai2L7JmeYvD_F0-r/view


## USAGE EXEMPLE


Une fois authentifié il est possible d'utiliser l'api de facon simple :

```python
api = ApiV5(
        api_base='api.helloasso.com',
        client_id=XXXXXX,
        client_secret=XXXXXX,
        timeout=60
    )

api.call("url", method="POST", data={...})
```

Il est également possible d'étendre la classe HaApiV5 pour ajouter vos propres méthodes, 
La classe AuthorizationApi peut servir d'exemple. (`helloasso_api/client/authorization`)

Créez une classe contenant vos appels :

```python

class OrganizationApi(object):
    def __init__(self, client):
        self._client = client

    def get_by_slug(self, slug: str) -> dict:
        return self._client.call(f"organizations/{slug}").json()
```

Puis créez une classe héritant de la classe HaApiV5 et référençant la nouvelle classe :

```python
class MyApi(HaApiV5):
    def __init__(self, *args, **kwargs):
        super(MyApi, self).__init__(*args, **kwargs)
        self.organization = OrganizationApi(self)

api = MyApi(
        api_base='api.helloasso.com',
        client_id=XXXXXX,
        client_secret=XXXXXX,
        timeout=60
)

api.authorization.generate_authorize_request(...)

...

api.organization.get_by_slug("test-asso")
```