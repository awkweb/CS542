require('../scss/styles.scss');
require('../index.html');

var React = require('react');
var ReactDOM = require('react-dom');

var App = React.createClass({

  render: function() {
    return (
      <h1>Hello, World :)</h1>
    );
  }
});

ReactDOM.render(
  <App />,
  document.getElementById("app")
);
