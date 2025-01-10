# Document Processing Service

This project provides a RESTful API to manage file uploads, image manipulations, and PDF conversions using Django and Django REST Framework.

## Features
- Upload files (images and PDFs).
- List, retrieve, and delete images or PDFs.
- Rotate images by a specified angle.
- Convert PDF files to other formats.

## Prerequisites
Ensure you have the following installed:
- Docker
- Docker Compose (optional for additional services)

## Project Setup

### 1. Build the Docker Image
To build the Docker image for this project, use the following command:
```bash
docker build -t document-processing-service .
```

### 2. Run the Docker Container
Run the Docker container with specific port mappings:
```bash
docker run -d -p 8000:8000 --name document-processing-service document-processing-service
```

- The application will be available at `http://localhost:8000`.

### 3. Create a Superuser
Before using the service, create a Django superuser:
```bash
docker exec -it document-processing-service python manage.py createsuperuser
```
Follow the prompts to set up the superuser credentials.

### 4. Obtain an Authentication Token
Use the following endpoint to obtain an authentication token for the superuser:
-**POST** `/api-token-auth/`

#### Request Schema
| Field       | Type     | Required | Description                |
|-------------|----------|----------|----------------------------|
| `username`  | `string` | Yes      | The username of the user.  |
| `password`  | `string` | Yes      | The password of the user.  |

Send the username and password as part of the request payload to retrieve the token.

## API Endpoints
### File Uploads
-**POST** `/upload/` - Upload an image or a PDF file.

#### Request Schema
| Field | Type      | Required | Description                                |
|-------|-----------|----------|--------------------------------------------|
| `pdf` | `file`    | No       | The PDF file to be uploaded.              |
| `image` | `file`  | No       | The image file to be uploaded.            |

At least one of `pdf` or `image` must be provided.

### Image Endpoints
-**GET** `/images/` - List all images for the authenticated user.

#### Response Schema
| Field       | Type     | Description                      |
|-------------|----------|----------------------------------|
| `title`     | `string` | The title of the image.          |
| `image`     | `string` | The URL of the uploaded image.   |
| `uploaded_at` | `datetime` | The upload timestamp.          |

-**GET** `/images/<id>/` - Retrieve a specific image.

#### Response Schema
| Field                | Type      | Description                      |
|----------------------|-----------|----------------------------------|
| `location`           | `string`  | The storage location of the image. |
| `width`              | `decimal` | The width of the image in pixels. |
| `height`             | `decimal` | The height of the image in pixels. |
| `number_of_channels` | `decimal` | The number of color channels.     |

-**DELETE** `/images/<id>/` - Delete a specific image.

-**POST** `/images/rotate/` - Rotate an image by a specified angle.

#### Request Schema
| Field   | Type      | Required | Description                     |
|---------|-----------|----------|---------------------------------|
| `angle` | `float`   | Yes      | The angle to rotate the image.  |
| `image` | `integer` | Yes      | The ID of the image to rotate.  |

### PDF Endpoints
-**GET** `/pdfs/` - List all PDFs for the authenticated user.

#### Response Schema
| Field       | Type     | Description                      |
|-------------|----------|----------------------------------|
| `title`     | `string` | The title of the PDF.            |
| `pdf`       | `string` | The URL of the uploaded PDF.     |
| `uploaded_at` | `datetime` | The upload timestamp.          |

-**GET** `/pdfs/<id>/` - Retrieve a specific PDF.

#### Response Schema
| Field            | Type      | Description                      |
|------------------|-----------|----------------------------------|
| `location`       | `string`  | The storage location of the PDF. |
| `number_of_pages` | `integer` | The number of pages in the PDF.  |
| `page_width`     | `decimal` | The width of each page in inches.|
| `page_height`    | `decimal` | The height of each page in inches.|

-**DELETE** `/pdfs/<id>/` - Delete a specific PDF.

-**POST** `/pdfs/convert/` - Convert a PDF to another format.

#### Request Schema
| Field   | Type      | Required | Description                    |
|---------|-----------|----------|--------------------------------|
| `pdf`   | `integer` | Yes      | The ID of the PDF to convert. |


## License
This project is licensed under the MIT License.

