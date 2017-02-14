var webpack = require('webpack');
module.exports = {
  entry: [
    "./client/travelPlanner.js",
  ],
  output: {
    path: __dirname + '/travel_planner/static',
    filename: "travelPlanner.js"
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
      },
      {test: /\.css$/, loader: 'style-loader!css-loader'}
    ]
  },
  plugins: [
  ]
};