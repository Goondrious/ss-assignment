# Picky Take-Home Assignment

## Original Description

Full stack Assignment
Image management and compression service

Your job will be to create a RESTful API service based on Fastapi that manages a database of images. A supporting UI web application written in NextJS or React should also be created to utilise a section of this API. The database is represented as a json file and images are stored locally on the file system.

Requirements

- Implement a simple CRUD interface for managing the data based on Fastapi.
- Given a larger image, the API should be able to accept and compress the image and return a downsized version in the http response
- Implement UI written in NextJS or React to allow the user to select and preview an uncompressed image to be compressed.
- Implement any other necessary UI components to allow the user to upload an uncompressed image to the API service created in earlier steps.
- Reusing the components created in earlier steps, display the uncompressed image generated by the API created in earlier steps.
- Document your project in a readme file

Bonus marks

- Package you application into a docker container by defining a dockerfile

Notes:

The purpose of this exercise is for us to evaluate and understand your software development processes and design choices. Besides Fastapi, you are free to choose the supporting libraries which will help you achieve the goal. You are welcome to take this exercise as far as you like. However, make sure to leave enough time to document your system thoroughly as it will help us understand your project and the intention behind your design decisions.

## System Design

High Level Functionality

- two-part image upload & compression = users upload raw images to the server. From these images, users make compressions based on `quality` (only jpeg) and `width` input. Constraints:
  - upload up to 10 images per user
  - upload up to 10 image compressions per image
  - 110 images total per user
- simple jwt authorization, using username+password for login

Database

```typescript
{
  users: { [userId]: User },
  images: { [userId]: { [imageId]: UserImage } }
  compressions: { [imageId]: { [compressionId]: UserImageCompression } }
}
```

- json database setup to primarily to use ids for lookups. No complex querying is supported
- nested keys are used for parent-child relationships:
  - all of a user's images are found in the `db.images[userId]` dictionary
  - all of an images compressions are found in the `db.compressions[imageId]` dictionary

File storage and access

- images and compressions are stored on the filesystem in `/filestore/{userId}/{imageName}` and `/filestore/{userId}/compressions/{compressionName}`
- files are accessed through signed urls with a short expiry time. Signatures are issued when new entities are created or when a user loads a related page (e.g. the user home page loads all their images)

## Shane's Dev Log

- I got acquianted with FastAPI by going through some tutorials
- I split up the project into frontend/backend then got a basic upload & compress function working
- I split the image upload route into upload and compress to get a feel for the process and added a simple json file db
- I went through the "Security tutorial" from FastAPI out of curiosity and added a slightly organic "auth flow" for the assignment
- I sketched out a minimal version of the CRUD routes and the associated frontend interactions. I had some very basic tests for the json db interactions
- I expanded the testing and refactored the backend code a bit
- I updated the frontend to map the new API and improved the overflow user flow and appearance

### TODO

- dockerization & cleanup scripts
  - proper db & fs init (via docker!)
- explore more intricate compression options
  - byte manipulation, 3rd-party api, color grading etc.
- frontend quality-of-life = more images, pagination, sorting, tagging & even a simple search

### Resources

- FastAPI docs
  - [Security tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- Pillow docs
- ChatGPT for high-level grokking
- a [good example of Fullstack FastAPI & React](https://github.com/fastapi/full-stack-fastapi-template/blob/master/docker-compose.yml)
