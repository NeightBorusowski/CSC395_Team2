Dev Chef’s Cookbook

Welcome to Dev Chef’s Cookbook. This software was created with the intention of communicating with a Large Language Model to generate a recipe, given a company name and ingredients by the user.

Prerequisites 

One of the most important prerequisites, is that, this project requires at minimum around 16GB of RAM in order to be able to safely communicate with the Large Language Model, without any issues. Using less RAM could cause complications. 

Be sure to have Docker engine installed on your machine. https://www.docker.com

In addition, be sure to have ollama downloaded locally on your machine, and run the command "ollama pull llama2"

Then import the .ollama folder into the “Flask_Server” folder, this .ollama folder should be located in your on the filepath "C:\Users\{username}\.ollama"

To run this, use this sequence of commands in the terminal.


cd .\Flask_Server\
docker-compose up --build 

Then, click on the, “http://127.0.0.1:5000” on the line 
recipe-app-container  |  * Running on http://127.0.0.1:5000


These commands sets up the Docker container and sets it on a localhost on port 5000, in order to communicate with the LLM.

Framework Description

There are two main services that are composed of, found in the “docker-compose.debug.yml”, 
“Ollama” and “flask-server.” These services are the containers that are being used throughout the project.

Flask-server: The created Python container which runs a Flask server in order to hold the backend logic for communication between the Ollama container and the frontend data display. To simplify, it works in the following way:

	1: Receives data from the frontend
	2: Creates a json object and creates a question based on the passed information from user.
	3: This question is then communicated to the the LLM, and generated
	4: After the response generation, the data is sent back to the frontend in order for it to be displayed on the results box.

This is a intricate process, because it involves the communication between the Large Language Model and the Frontend page. 

Ollama: This is a very essential part of the project. This service sets up the ollama container so that the Large Language Model can be run locally on your machine. Flask-server connects this piece with the LLM.

Be sure to note the compose file for the versions used, and the different ports that are being used and ran on the user’s machine.

Use of Application

The docker-compose.yml opens port 5000 to the local host in order to be able to effectively connect the Flask server container to the web browser. Here is what Dev Chef’s Cookbook looks like pictorially. 


![image](https://github.com/user-attachments/assets/0d965056-8de2-4b94-9631-4ec02f0b8e17)



Using Dev Chefs Cookbook Example




First, select the drop down of the company you would like to use. 
Next, input the ingredients, and choose an LLM.
After doing this, hit submit and wait until response is generated!

![image](https://github.com/user-attachments/assets/87e5869f-0178-499f-8b8c-a28b833cb699)



Example recipe!


![image](https://github.com/user-attachments/assets/12b22b33-25df-4cf4-ba86-9455a9966b16)




Additional Features

Below will be any additional updates to the project, be sure to check here and ensure your version is up to date.
