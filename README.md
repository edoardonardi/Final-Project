# Final-Project

Team Members:
Edoardo Nardi
Jonathan Amitai


# **Portfolio Performance Tracker**
The **Portfolio Performance Tracker** is designed to simplify investment tracking for individuals managing a portfolio of stocks, cryptocurrencies, and commodities. Instead of manually tracking each asset, this web application automates the process of gathering real-time and historical data, calculating the value of each asset, and providing a clear overview of your overall portfolio performance. Using an API Key from AlphaVantage, our website is able to track stock prices and data. 

### Use Case Example
Imagine you have invested in Apple stock, or another asset in the stock market. Tracking the fluctuating values of these assets can be overwhelming. This application allows you to input each asset, specify its purchase price and date, and then sit back while the app retrieves real-time prices and calculates how well your portfolio is performing. With an easy-to-use web interface, users can see their portfolio performance metrics at a glance.
   
### How To Use Appliation
Our application can be used through our Website URL which was made using render. The link for use is https://edojonathanportfoliotracker.onrender.com/ .

If the link above is not working due to API request limits, please 

1. **Run the Flask Application**:
   ```bash
   flask run
   ```
   The application will be accessible at `http://127.0.0.1:5000/`.

2. **Access the Web Interface**:
   - Open your web browser and navigate to `http://127.0.0.1:5000/`.
   - Use the interface to add assets to your portfolio and view performance metrics.

### Portfolio example
This is an example of what you see when you go on our website, where you manually input stock information and add to your portfolio.
![Portfolio Summary](https://github.com/edoardonardi/final_project/blob/main/Screenshot%20(23).png?raw=true)




Once added to portfolio, you can view your entire portfolio and track it directly in the website.



![Portfolio Tracker Homepage](https://github.com/edoardonardi/final_project/blob/main/Screenshot%20(22).png?raw=true)

### External Assistance
After manually creating our API Key and beginning to build our code, we began using GENAI to structure our code and begin to set up our app which would eventually run on our website. We used ChatGPT to add features such as structuring our portfolio, including stating Current Price, Purchase Price, Current Value, and percent change for each stock added to the porfolio. We did struggle with the API key for CoinGecko, which was part of our initial goal of having Stocks and Cryptocurrencies both present in our website. We also asked chatGPT to assist with structuring our frontend HTML code, as well as going back and forth between ChatGPT and Render for our website creation, in which we added applications to our requirements.txt file and were able to run commands for Render.

### Other Issues
Since we have a limit for 25 daily uses for our API Key, there may be issues when trying to get stock data if there are too many uses daily in the website.





