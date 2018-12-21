import axios from 'axios'

let $backend = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
})

$backend.defaults.xsrfHeaderName = "X-CSRFToken"
$backend.defaults.xsrfCookieName = 'csrftoken'


// Response Interceptor to handle and log errors
$backend.interceptors.response.use(function (response) {
    return response
}, function (error) {
    // eslint-disable-next-line
    console.log(error)
    return Promise.reject(error)
})

$backend.$fetchLocale = () => {
    return $backend.get(`/locale/`)
        .then(response => response.data)
}

$backend.$fetchFilters = (lang, currencyCode) => {
    return $backend.get(`/filters/?language=${lang}&currency=${currencyCode}`)
        .then(response => response.data)
}

$backend.$fetchDorms = (lang, currency) => {
    return $backend.post(`/dorms/`, {
        currency: currency,
        language: lang
    })
        .then(response => response.data)
},
    $backend.$searchDorms = (filters) => {
        return $backend.post(`/dorms/`, {
            currency: filters.currency,
            language: filters.lang,
            category_selected_option_id: filters.category,
            duration_option_id: filters.duration,
            dorm_features: filters.dormFeatures,
            room_features: filters.roomFeatures,
            additional_filters: filters.additionalFilters
        })
            .then(response => response.data)
    }

$backend.$fetchDorm = (dormId, lang, currencyCode) => {
    return $backend.get(`/dorms/${dormId}/?language=${lang}&currency=${currencyCode}`)
        .then(response => response.data)
}

// $backend.$login = () => {
//   return $backend.get(`/login`)
//       .then(response => response.data)
// }

$backend.$login = (user) => {
    return $backend.post(`/auth/login/`, {
        email: user.email,
        password: user.password
    })
        .then(response => response.data)
}

$backend.$auth = () => {
    return $backend.get(`/auth/user/`)
        .then(response => response.data)
}

$backend.$register = (user) => {
    return $backend.post(`/auth/registration/`, {
        name: user.name,
        email: user.email,
        password1: user.password,
        password2: user.password
    })
        .then(response => response.data)
}

$backend.$reserveRoom = (roomId) => {
    return $backend.post(`/reservations/`, {
        room_id: roomId
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
    return $backend.get(`/reservation/`)
        .then(response => response.data)
}

$backend.$verifyEmail = (key) => {
    return $backend.post(`/auth/registration/verify-email/`, {
        key: key
    })
        .then(response => response.data)
}

$backend.$resendVerifyEmail = (email) => {
    return $backend.post(`/auth/resend-confirmation/`, {
        email: email
    })
        .then(response => response.data)
}

$backend.$resetPassword = (email) => {
    return $backend.post(`/auth/password/reset/`, {
        email: email
    })
        .then(response => response.data)
}

$backend.$resetPasswordConfirm = (data) => {
    return $backend.post(`/auth/password/reset/confirm/`, {
        uid: data.userID,
        key: data.key,
        new_password1: data.password,
        new_password2: data.password
    })
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
