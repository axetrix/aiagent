import React, { useState, useEffect } from 'react';

function App() {
  const [account, setAccount] = useState(null);
  const [error, setError] = useState(null);
  const apiKey = 'YOUR_ETHERSCAN_API_KEY'; // Replace with your actual Etherscan API key

  useEffect(() => {
    const fetchAccountData = async () => {
      try {
        // Generate a random Ethereum address (for demonstration purposes)
        const randomAddress = '0x' + Math.random().toString(36).substring(2, 42);

        //Etherscan API endpoint for account balance
        const apiUrl = `https://api.etherscan.io/api?module=account&action=balance&address=${randomAddress}&tag=latest&apikey=${apiKey}`;
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        if (data.status === "1") {
          // Assuming the API returns a JSON object with a "result" field
          setAccount({ address: randomAddress, balance: data.result });
          setError(null);
        } else {
          setError(data.message || "Error fetching account data");
          setAccount(null);
        }

      } catch (e) {
        setError(e.message);
        setAccount(null);
      }
    };

    fetchAccountData();
  }, []);

  return (
    <div>
      <h1>Random Ethereum Account Info</h1>
      {error && <p>Error: {error}</p>}
      {account ? (
        <div>
          <p>Address: {account.address}</p>
          <p>Balance: {account.balance} Wei</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;