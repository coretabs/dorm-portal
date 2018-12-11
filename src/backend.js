import axios from 'axios'

let $backend = axios.create({
  baseURL: 'http://localhost:3000',
  timeout: 5000,
  headers: {'Content-Type': 'application/json'}
})

// Response Interceptor to handle and log errors
$backend.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // eslint-disable-next-line
  console.log(error)
  return Promise.reject(error)
})

$backend.$fetchLocale = () => {
  return $backend.get(`/locale`)
      .then(response => response.data)
}

$backend.$fetchFilters = (lang,currencyCode) => {
  return $backend.get(`/filter?language=${lang}&currency=${currencyCode}`)
      .then(response => response.data)
}

$backend.$fetchDorms = () => {
  return $backend.get(`/dorms`)
      .then(response => response.data)
}

$backend.$fetchDorm = (dormId) => {
  return $backend.get(`/dorms/${dormId}`)
      .then(response => response.data)
}

$backend.$login = () => {
  return $backend.get(`/login`)
      .then(response => response.data)
}

$backend.$reserveRoom = (roomId) => {
  return $backend.post(`/reservations`,{
    room_id : roomId
  })
  .then(response => response.data)
}

// $backend.$fetchReservation = (reservationID) => {
//   return $backend.post(`/reservation`,{
//     reservation_id : reservationID
//   })
//   .then(response => response.data)
// }

$backend.$fetchReservation = () => {
  return $backend.get(`/reservation`)
      .then(response => response.data)
}


$backend.$postMessage = (payload) => {
    return $backend.post(`messages/`, payload)
        .then(response => response.data)
}

$backend.$deleteMessage = (msgId) => {
    return $backend.delete(`messages/${msgId}`)
        .then(response => response.data)
}

export default $backend
