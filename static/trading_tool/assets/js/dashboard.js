$(function () {
  // Initialize positions_data with an empty object if not available
  
  console.log("positions_datapositions_data", positions_data)

  // Check if netPositions is available in positions_data and is an array
  if (Array.isArray(positions_data.netPositions)) {
      var realized_profits = [];
      var realized_loss = [];

      positions_data.netPositions.forEach(function (position) {
          var rounded_profit = Math.round(position.realized_profit * 100) / 100;
          if (rounded_profit >= 0) {
              realized_profits.push(rounded_profit);
              realized_loss.push(0);
          } else {
              realized_loss.push(-rounded_profit);
              realized_profits.push(0);
          }
      });

      // Extracting last 7 characters of each symbol string into another array
      var symbols_data = positions_data.netPositions.map(function (position) {
          return position.symbol.slice(-7);
      });

      // Sort the arrays in ascending order
      realized_profits.sort(function (a, b) {
          return a - b;
      });

      realized_loss.sort(function (a, b) {
          return a - b;
      });

      // Find the maximum value in the arrays
      var max_profit = Math.max(...realized_profits);
      var max_loss = Math.max(...realized_loss);
      var max_value = Math.max(max_profit, max_loss);

      // Round up to the nearest hundred higher than the maximum value
      var rounded_profit = Math.ceil(max_value / 100) * 100;

      // Assign chart options
      var chart = {
          // Your chart options here...
      };

      // Render the chart
      var chart = new ApexCharts(document.querySelector("#chart"), chart);
      chart.render();
  } else {
      // If netPositions is not available or not an array, initialize empty arrays
      var realized_profits = [];
      var realized_loss = [];
      var symbols_data = [];
  }

  // Handle exceptions for the other sections similarly...
});