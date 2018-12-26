import axios from 'axios'

let $backend = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true
})

$backend.defaults.xsrfHeaderName = "X-CSRFToken"
$backend.defaults.xsrfCookieName = 'csrftoken'

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

$backend.$fetchReservation = (id) => {
    return $backend.get(`/reservations/${id}`)
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


$backend.$uploadReceipt = (id, formData) => {
    return $backend.post(`/reservations/${id}/receipts/`, formData)
    .then(response => response.data)
}


$backend.$fetchManagerDorms = () => {
    return $backend.get(`/manager-dorms/`)
        .then(response => response.data)
}

$backend.$fetchManagerReservation = (id) => {
    return $backend.get(`/manager-dorms/${id}/reservations/`)
        .then(response => response.data)
}

$backend.$fetchManagerDorm = (id) => {
    return $backend.get(`/manager-dorms/${id}`)
        .then(response => response.data)
}

$backend.$updateReservationStatus = (data) => {
    return $backend.put(`/manager-dorms/${data.dormID}/reservations/${data.reservationID}/`,{
        status: data.status,
        confirmation_deadline_date: data.deadline,
        follow_up_message: data.message
    })
    .then(response => response.data)
}

$backend.$updateDormInfo = (data) => {
    return $backend.put(`/manager-dorms/${data.dormID}/`,{
        abouts: data.abouts,
        contact_name: data.contact_name,
        contact_number: data.contact_number,
        contact_fax: data.contact_fax,
        contact_email: data.contact_email,
        features: data.features,
        geo_longitude: data.geo_longitude,
        geo_latitude: data.geo_latitude,
        address: data.address
    })
    .then(response => response.data)
}



$backend.$deleteMessage = (msgId) => {
    return $backend.delete(`messages/${msgId}`)
        .then(response => response.data)
}

export default $backend
