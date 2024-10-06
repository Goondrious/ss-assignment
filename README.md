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

# Shane's Dev Log

- just getting acquianted with FastAPI by going through the basic tutorials!
- split up the project into frontend/backend to get a basic upload & compress function working
- did a basic image upload route to get a feel for the process and added a simple json file db
- went through the "Security tutorial" from FastAPI just to get a feel and have a slightly organic "user flow" for the assignment
- I sketched out a minimal version of the CRUD routes and the associated frontend interactions. I had some very basic tests for the json db interactions
- I expanded the tests and refactored the backend code a bit

## Resources

- FastAPI docs
  - [Security tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- Pillow docs
- ChatGPT for high-level grokking
- a [good example of Fullstack FastAPI & React](https://github.com/fastapi/full-stack-fastapi-template/blob/master/docker-compose.yml)
