import axios from 'axios'

let $backend = axios.create({
    baseURL: 'https://dorm-portal.herokuapp.com/api',
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

$backend.$uploadPhotos = (id, formData) => {
    return $backend.post(`/manager-dorms/${id}/photos/`, formData)
        .then(response => response.data)
}

$backend.$upload360Photos = (id, data) => {
    return $backend.post(`/manager-dorms/${id}/photos/`, {
        is_3d: data.is360Photo,
        url: data.url
    })
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
    return $backend.get(`/manager-dorms/${id}/`)
        .then(response => response.data)
}

$backend.$fetchManagerDormRooms = (id) => {
    return $backend.get(`/manager-dorms/${id}/rooms/`)
        .then(response => response.data)
}



$backend.$updateReservationStatus = (data) => {
    return $backend.put(`/manager-dorms/${data.dormID}/reservations/${data.reservationID}/`, {
        status: data.status,
        confirmation_deadline_date: data.deadline,
        follow_up_message: data.message
    })
        .then(response => response.data)
}

$backend.$updateDormInfo = (data) => {
    return $backend.put(`/manager-dorms/${data.dormID}/`, {
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

$backend.$updateDormCover = (id, formData) => {
    return $backend.put(`/manager-dorms/${id}/update-cover/`, formData)
        .then(response => response.data)
}

$backend.$addBankAccount = (id, data) => {
    return $backend.post(`/manager-dorms/${id}/bank-accounts/`, {
        bank_name: data.name,
        account_name: data.accountName,
        account_number: data.accountNumber,
        swift: data.swift,
        iban: data.iban,
        currency_code: data.currency
    })
        .then(response => response.data)
}

$backend.$deleteBankAccount = (dormId, accountId) => {
    return $backend.delete(`/manager-dorms/${dormId}/bank-accounts/${accountId}`)
        .then(response => response.data)
}
$backend.$deleteDormPhoto = (dormId, photoId) => {
    return $backend.delete(`/manager-dorms/${dormId}/photos/${photoId}`)
        .then(response => response.data)
}
$backend.$deleteDormRoom = (dormId, roomId) => {
    return $backend.delete(`/manager-dorms/${dormId}/rooms/${roomId}`)
        .then(response => response.data)
}
$backend.$updateBankAccount = (dormId, accountId, data) => {
    return $backend.put(`/manager-dorms/${dormId}/bank-accounts/${accountId}/`, {
        bank_name: data.name,
        account_name: data.accountName,
        account_number: data.accountNumber,
        swift: data.swift,
        iban: data.iban,
        currency_code: data.currency
    })
        .then(response => response.data)
}

$backend.$fetchRoomFilters = () => {
    return $backend.get(`/manager-dorms/filters/`)
        .then(response => response.data)
}

$backend.$addNewRoom = (id, data) => {
    return $backend.post(`/manager-dorms/${id}/rooms/`, {
        total_quota: data.totalQuota,
        allowed_quota: data.allowedQuota,
        room_type_id: data.roomTypeId,
        people_allowed_number: data.peopleAllowedNumber,
        price: data.price,
        currency_id: data.currencyId,
        room_confirmation_days: data.confirmationDays,
        duration_id: data.durationId,
        room_features: data.roomFeatures,
        radio_options: data.radioChoices,
        integral_choices: data.integralChoices
    })
        .then(response => response.data)
}

$backend.$askForReview = (dormId,reservationId) => {
    return $backend.post(`/manager-dorms/${dormId}/reservations/${reservationId}/ask-review/`)
        .then(response => response.data)
}

$backend.$submitReview = (dormId,data) => {
    return $backend.post(`/reservations/${dormId}/reviews/`,{
        stars: data.stars,
        description: data.comment
    })
        .then(response => response.data)
}



export default $backend
