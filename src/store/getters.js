export default {
  lang: state => {
    const currentLang = state.language
    const lang = require(`../../locale/lang.${currentLang}.json`);
    return lang[currentLang]
  },
  activeCurrency: state => state.currencySymbol,
  isLoggedIn: state => !!state.isAuth,
  isAdmin: state => !!state.isAdmin,
  authStatus: state => state.authStatus,
  reservationData: state => state.reservation,
  managerDorms: state => state.managerDorms,
  managerDormRooms: state => state.managerDormRooms,
  adminActiveComponent: state => state.adminActiveComponent,
  drawer: state => state.drawer,
  manageReservation: state => state.manageReservation,
  manageDorm: state => state.manageDorm,
  snackbar: state => state.snackbar,
  reservationStepperState: state => state.reservationStepperState
}