### Challnge detailes

<details>
  <summary>Part A: Python Token Server</summary>
  
Write a command line program in Python + Django \ Flask that would do the following:
1.	Implement a server that will listen for API calls
2.	The server should support multiple clients to connect
3.	The server should expose the following APIs:
    * a.	“Register client”
          - Receive a JSON request containing username + password.
          - Return JWT access token.
          - Store (in memory) list of all users that were granted a token.
  
    * b.	“Show client list”
          - Return list of all registered users
    * c.	“Authorize client”
          - Receive JWT access token
          - Verify that the token is valid, return result.
4.	The server should log (on command line) received connections and performed actions
5.	Write tests to cover the functionality
</details>

<details>
  <summary>Part B: Python Communication Server</summary>

Write a command line program in Python + Django \ Flask that would do the following:
1.	Implement a server that will listen for API calls
2.	The server should support multiple clients to connect
3.	The server should support the following APIs:
a.	“Echo”
Send received text back to the caller
b.	“Time”
Send current date + time to the caller
4.	Each API expects to receive a JWT access token.
5.	Before replying to the clients, the server should contact the Python Token Server (Part A in this task) in order to verify the received token.
6.	The server should log (on command line) received connections and performed actions
7.	Write tests to cover the functionality
</details>

<details>
  <summary>Part C: Python Client</summary>

Write a command line program in Python that would do the following:
1.	Implement a client that communicates with a serve.
2.	The client should receive the address of the Communication Server (part B) and Token Server (part A) as command line arguments
3.	The client should connect to the Token server to obtain a JWT access token
4.	The client should connect to the Communication Server and wait for a keyboard command:
a.	If the desired action is “Echo”
    * i.	Receive text from keyboard.
    * ii.	Send the server a call to the “Echo” API with the content.
    * iii.	Display received result.
b.	If the desired action is “Time”
i.	Send the server a call to the “Time” API.
ii.	Display received result.
5.	Write tests to cover the functionality
</details>
