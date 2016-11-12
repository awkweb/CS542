import axios from 'axios'

function fetch (endpoint) {
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
  return fetch('/api/dish/all')
}