# T2A2 - API Webserver

## Coder Academy Term 2 Assignment 2

Student Name: Fabian Sugandhi\
[Github Repo](https://github.com/FabSugandhi/FabianSugandhi_T2A2)

## Installation and Running API Instructions

### Database Setup

1. Ensure that PostgreSQL, Python, and Pip are installed. Skip this step if you have them installed or refer to the following links for installation instructions:
    - [PostgreSQL Installation](https://www.postgresql.org/docs/current/tutorial-install.html)
    - [Python Installation](https://www.python.org/downloads/)
    - [Pip Installation](https://pip.pypa.io/en/stable/installation/)

2. Open a new terminal window. Navigate to __FabianSugandhi_T2A2/src__ directory in your terminal. Then, create a virtual environment with these commands:

    ```
    python3 -m venv venv
    ```
    
    Then activate it with:

    ```
    source venv/bin/activate
    ```

3. Next, install the dependencies using:

    ```
    pip install -r requirements.txt
    ```

4. Once the dependencies are installed, start PostgreSQL from your terminal.

    For WSL, in the terminal, start PostgreSQL with:

    ```
    sudo -u postgres psql
    ```

    For MacOS, in the terminal, start PostgreSQL with:

    ```
    psql postgres
    ```

5. With PostgreSQL, create a new database with this command:

    ```
    CREATE DATABASE <db_name>
    ```

    Replace the &lt;db_name&gt; with your choice of database name. For the purpose of this documentation, the database name is assumed to be __pokemontcg_db__.

6. Create a new __.flaskenv__ file in the __src__ directory and COPY and PASTE the code in the __.flaskenv.sample__ file into it, then you are free to adjust each field according to your configuration preferences.

7. Create a new __.env__ file in the __src__ directory and COPY and PASTE the code in the __.env.sample__ file into it, then you are free to adjust each field according to your configuration preferences.

8. Next, go back into your terminal and run the following commands to create and seed the tables in the database:

    ```
    flask db create
    ```

    ```
    flask db seed
    ```
    And run the following command to run the API client:
    ```
    flask run
    ```

9. Use your preferred API client to run and test the API. This project was tested using __Bruno__. You can install it from this [link](https://www.usebruno.com/downloads). Use localhost:<flask_run_port_value> in the URL. As an example, the testing of this API was performed using this address: _127.0.0.1:5000/_.

10. Go into the __blueprint__ directory and open each of the "__&lt;name&gt;-bp.py__" files within to find the available routes.

## R1: Explain the problem that this app will solve, and explain how this app solves or addresses the problem

While Pokemon TCG is one of the most popular Trading Card Game today, it is not without problems. As one of the biggest and one of the longest running name in the Trading Card Game scene, the Pokemon TCG has a very extensive card library, with cards of the same name sometimes having different versions coming from different sets. It is also becomes the game standard for the players to play multiple copies of some of the important cards in their decks. Also, some players prefer to not have to buy too many additional copies of specific cards, just because they want to be including them in multiple decks, rather just swapping them between the decks they are currently playing.

All these factors make it a very arduous task for the players to manually keep track of what cards they already have and which decks have they included each card to, something that might keep newer players away from exploring the game. This app is developed in order to alleviate some of those issues.

The purpose and main function of this app is to assist Pokemon TCG players trying to keep track of their card collections, as well as how many decks they have and which cards are included in each of their deck. By utilising this app, the players won't have to manually write each of their deck recipe on paper as usually done in the game's early days. Instead, they will be able to quickly and efficiently record their cards and decks into the app, with them always having the option to update their collections or adjust their deck recipes by utilising the app's functionalities. Additionally, the players also won't have to worry about inputting the wrong cards, since this application is seeded with the official list of legal cards and sets in the game's standard format. This means that as long as the player knows the name of the card and which set it comes from, the app automatically notes the information down for the player. This function helps the players remember which version of the card they already have or are playing in their deck when they are checking their decks recipes after they made them, which is very helpful when they have multiple decks and a larger card collection size.

This app will be designed so that it can be used flexibly in multiple platforms and by various users. For example, it can be utilised in a community website for Pokemon TCG players to share their collections, or maybe developed into an independent personal website for players who want to keep it simple and private.

## R2: Describe the way tasks are allocated and tracked in your project

NEED TO BE DONE

## R3: List and explain the third-party services, packages and dependencies used in this app

NEED TO BE DONE

## R4: Explain the benefits and drawbacks of this app’s underlying database system

This application was developed using PostgreSQL as the database management system.

One reason for choosing this system is its robustness. PostgreSQL is an ACID (Atomicity, Consistency, Isolation, Durability) compliant Database Management Systems (DBMS), ensuring that all database transactions are processed reliably and prioritizing data integrity (Singh, 2023). Some example of its data integrity mechanism includes data types, triggers, and constraints. Furthermore, PostgreSQL's write-ahead logging minimizes the possibility of data loss (Peterson, 2024). Data integrity is a crucial aspect for systems like this collection tracker application, whose main purpose is to accurately manage and records data on each of its users' deck and card collections, in order to improve their quality of life by making it easy to find and retrieve the records. PostgreSQL also has useful features, such as constraints, that helps to ensure that each items are categorized and named accordingly, making search functionalities much more reliable for people trying to check specific cards.






## Reference List

Peterson, R. (2024). _What is PostgreSQL? Introduction, advantages & disadvantages_. Guru99. https://www.guru99.com/introduction-postgresql.html

Singh, G. (2023). _The power of PostgreSQL: a comprehensive exploration_. Vertisystem. https://vertisystem.medium.com/the-power-of-postgresql-a-comprehensive-exploration-dba09e0e030c