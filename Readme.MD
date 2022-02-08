
## API Reference

#### Generate Short url

```http
  POST /genUrl
```

| Request Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `{"url":"url to be shortened"}` | `Json` | You get a shorturl |

#### Regenerate Short url
```http
  PUT /genUrl
```

| Request Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `{"url":"url to be shortened"}` | `Json` | You get a new regenerated shorturl |

#### Get short url 

```http
  GET /genUrl
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `url`      | `string` | **Required**. original url to fetch shorturl|


## Run Locally

Clone the project

```bash
  git clone https://github.com/Adarsh154/Urlredirect.git
```

Go to the project directory

```bash
  cd Urlredirect
```

Start the server

```bash
  docker-compose up
```