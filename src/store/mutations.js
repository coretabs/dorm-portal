import $backend from '@/backend';

export default {
  updateSnackbar(state, payload) {
    state.snackbar.trigger = true
    state.snackbar.message = payload.message
    state.snackbar.color = payload.color
  },
  fetchLocale(state, responseDate) {
    state.currencies = responseDate.currencies;
    state.languages = responseDate.languages;
    localStorage.setItem("currency-code", responseDate.currencies[0].code);
    localStorage.setItem("currency-symbol", responseDate.currencies[0].symbol);
  },
  fetchFilters(state, responseDate) {
    state.filters = responseDate;
  },
  fetchDorms(state) {
    $backend.$fetchDorms(state.currencyCode).then(responseDate => {
      state.dorms = responseDate;
    });
  },
  fetchSearchedDorms(state) {
    let filters = {
      lang: state.language,
      currency: state.currencyCode,
      duration: state.userFilters.duration,
      category: state.userFilters.category,
      dormFeatures: state.userFilters.dorm_features,
      roomFeatures: state.userFilters.room_features,
      additionalFilters: state.userFilters.additional_filters
    }
    $backend.$searchDorms(filters).then(responseDate => {
      state.dorms = responseDate;
    });
  },
  auth_success(state) {
    state.authStatus = 'Success'
    state.isAuth = !!localStorage.getItem('auth')
    state.isAdmin = localStorage.getItem('admin')
  },
  auth_error(state) {
    state.authStatus = 'An error occur'
  },
  logout(state) {
    state.isAuth = null
    state.isAdmin = null
  },
  registerSuccess(state) {
    state.authStatus = 'Registeration Faild'
  },
  reserveRoom(state, { room, responseDate }) {
    localStorage.setItem("room", JSON.stringify({ room }))
    localStorage.setItem('auth', JSON.stringify({
      user_name: responseDate.user.name,
      reservarion_id: responseDate.id,
      current_step: responseDate.user.current_step
    }))
  },
  fetchReservation(state, responseDate) {
    state.reservation = responseDate;
  },
  fetchManagerDorms(state, responseDate) {
    state.managerDorms = responseDate
  },
  fetchManagerDormRooms(state, responseDate) {
    state.managerDormRooms = responseDate
  },
  fetchManagerReservation(state, responseDate) {
    state.manageReservation = responseDate
  },
  fetchManagerDorm(state, responseDate) {
    state.manageDorm = responseDate
    let selectFeaturesHolder = []
    for (const feature of responseDate.features) {
      selectFeaturesHolder.push(feature.id)
    }
    state.dormFeatures = selectFeaturesHolder
  }
}