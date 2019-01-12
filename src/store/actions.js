import $backend from '@/backend';

export default {
  fetchLocale({ commit }) {
    $backend.$fetchLocale().then(responseDate => {
      commit('fetchLocale', responseDate);
    });
  },
  fetchFilters({ commit }, currentCurrency) {
    return new Promise((resolve, reject) => {
      $backend.$fetchFilters(currentCurrency).then(responseDate => {
        commit('fetchFilters', responseDate);
        resolve(responseDate)
      })
        .catch(err => {
          reject(err)
        })
    })
  },
  fetchDorms({ commit }) {
    commit('fetchDorms');
  },
  fetchSearchedDorms({ commit }, data) {
    return new Promise((resolve) => {
      $backend.$searchDorms(data).then(responseDate => {
        commit('fetchSearchedDorms', responseDate);
        resolve(responseDate)
      })
    })
  },
  auth({ commit }) {
    return new Promise((resolve, reject) => {
      $backend.$auth().then(responseDate => {
        if (responseDate.is_manager) {
          localStorage.setItem('admin', true)
        }
        localStorage.setItem('auth', JSON.stringify({
          user_name: responseDate.name,
          reservarion_id: responseDate.reservation_id,
          current_step: responseDate.current_step
        }))
        commit('auth_success')
        resolve(responseDate)
      })
        .catch(err => {
          localStorage.removeItem('admin')
          localStorage.removeItem('auth')
          commit('auth_error')
          reject(err)
        })
    })
  },
  logout({ commit }) {
    return new Promise((resolve) => {
      commit('logout')
      localStorage.removeItem('auth')
      localStorage.removeItem('admin')
      resolve()
    });
  },
  reserveRoom({ commit }, room) {
    return new Promise((resolve, reject) => {
      $backend.$reserveRoom(room.id).then(responseDate => {
        commit('reserveRoom', { room, responseDate })
        resolve(responseDate)
      })
        .catch(err => {
          reject(err)
        })
    });
  },
  fetchReservation({ commit }, id) {
    $backend.$fetchReservation(id).then(responseDate => {
      commit('fetchReservation', responseDate)
    });
  },
  register({ commit }, user) {
    return new Promise((resolve, reject) => {
      $backend.$register(user).then(responseDate => {
        commit('registerSuccess')
        resolve(responseDate)
      })
        .catch(err => {
          reject(err)
        })
    })
  },
  fetchManagerDorms({ commit }) {
    return new Promise((resolve, reject) => {
      $backend.$fetchManagerDorms().then(response => {
        commit('fetchManagerDorms', response)
        resolve(response)
      }).catch(err => {
        reject(err)
      })
    })
  },
  fetchManagerReservation({ commit }, id) {
    return new Promise((resolve, reject) => {
      $backend.$fetchManagerReservation(id).then(response => {
        commit('fetchManagerReservation', response)
        resolve(response)
      }).catch(err => {
        reject(err)
      })
    })
  },
  fetchManagerDorm({ commit }, id) {
    return new Promise((resolve, reject) => {
      $backend.$fetchManagerDorm(id).then(response => {
        commit('fetchManagerDorm', response)
        resolve(response)
      }).catch(err => {
        reject(err)
      })
    })
  },
  fetchManagerDormRooms({ commit }, id) {
    return new Promise((resolve, reject) => {
      $backend.$fetchManagerDormRooms(id).then(response => {
        commit('fetchManagerDormRooms', response)
        resolve(response)
      }).catch(err => {
        reject(err)
      })
    })
  }
}