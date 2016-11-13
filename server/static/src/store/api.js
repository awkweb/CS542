import axios from 'axios'

function get (endpoint) {
    return new Promise((resolve, reject) => {
      axios.get(endpoint)
      .then(function (response) {
        resolve(response.data)
      })
      .catch(function (error) {
        reject(error)
      });
    })
}

export function fetchDishes () {
  return get('/api/dish/all')
}