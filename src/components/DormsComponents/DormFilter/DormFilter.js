import DormCard from "../DormCard/DormCard.vue";
import DormSearch from "../DormSearch/DormSearch.vue";
export default {
  name: "DormFilter",
  components: {
    "dorm-card": DormCard,
    "dorm-search": DormSearch
  },
  data: function () {
    return {
      dorms: [{
        id: "1",
        name: "Alfam Dorm",
        cover: "https://images.pexels.com/photos/1082326/pexels-photo-1082326.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
        stars: "4",
        number_of_reviews: "128",
        geo_longitude: "35.14745",
        geo_latitude: "33.90707",
        address: "Next to computer facuilty",
        number_of_found_rooms: "9",
        features: [{
          icon: "fa-wifi",
          name: "free wifi"
        },
        {
          icon: "fa-parking",
          name: "free parking"
        },
        {
          icon: "fa-shower",
          name: "Shower"
        },
        {
          icon: "fa-wind",
          name: "Air condition"
        },
        {
          icon: "fa-wifi",
          name: "free wifi"
        },
        {
          icon: "fa-parking",
          name: "free parking"
        },
        {
          icon: "fa-shower",
          name: "Shower"
        },
        {
          icon: "fa-wind",
          name: "Air condition"
        },
        {
          icon: "fa-wifi",
          name: "free wifi"
        },
        {
          icon: "fa-parking",
          name: "free parking"
        },
        {
          icon: "fa-shower",
          name: "Shower"
        },
        {
          icon: "fa-wind",
          name: "Air condition"
        }
        ],
        rooms: [
          {
            "id": 5,
            "room_type": "single room",
            "photos": [
              "https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
              "https://images.pexels.com/photos/439227/pexels-photo-439227.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
              "https://images.pexels.com/photos/271734/pexels-photo-271734.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
              "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            ],
            "rooms_left": 5,
            "price": 500,
            "people_number": 2,
            "features": [
              {
                name: "free Wifi",
                icon: "fa-wifi"
              },
              {
                  name: "Restaurant",
                  icon: "fa-utensils"
              },
              {
                  name: "Laundry",
                  icon: "local_laundry_service"
              },
              {
                name: "Market",
                icon: "fa-shopping-cart"
              },
              {
                name: "Elevator",
                icon: "fa-check"
              },
              {
                name: "Air condition",
                icon: "fa-wind"
              },
              {
                name: "Fire alarm",
                icon: "fa-fire"
              },
              {
                name: "Barber",
                icon: "fa-cut"
              },
              {
                name: "free Wifi",
                icon: "fa-wifi"
              },
              {
                  name: "Restaurant",
                  icon: "fa-utensils"
              },
              {
                  name: "Laundry",
                  icon: "local_laundry_service"
              },
              {
                name: "Market",
                icon: "fa-shopping-cart"
              },
              {
                name: "Elevator",
                icon: "fa-check"
              },
              {
                name: "Air condition",
                icon: "fa-wind"
              },
              {
                name: "Fire alarm",
                icon: "fa-fire"
              },
              {
                name: "Barber",
                icon: "fa-cut"
              },
              {
                name: "free Wifi",
                icon: "fa-wifi"
              },
              {
                  name: "Restaurant",
                  icon: "fa-utensils"
              },
              {
                  name: "Laundry",
                  icon: "local_laundry_service"
              },
              {
                name: "Market",
                icon: "fa-shopping-cart"
              },
              {
                name: "Elevator",
                icon: "fa-check"
              },
              {
                name: "Air condition",
                icon: "fa-wind"
              },
              {
                name: "Fire alarm",
                icon: "fa-fire"
              },
              {
                name: "Barber",
                icon: "fa-cut"
              },
              {
                name: "free Wifi",
                icon: "fa-wifi"
              },
              {
                  name: "Restaurant",
                  icon: "fa-utensils"
              },
              {
                  name: "Laundry",
                  icon: "local_laundry_service"
              },
              {
                name: "Market",
                icon: "fa-shopping-cart"
              },
              {
                name: "Elevator",
                icon: "fa-check"
              },
              {
                name: "Air condition",
                icon: "fa-wind"
              },
              {
                name: "Fire alarm",
                icon: "fa-fire"
              },
              {
                name: "Barber",
                icon: "fa-cut"
              },{
                name: "free Wifi",
                icon: "fa-wifi"
              },
              {
                  name: "Restaurant",
                  icon: "fa-utensils"
              },
              {
                  name: "Laundry",
                  icon: "local_laundry_service"
              },
              {
                name: "Market",
                icon: "fa-shopping-cart"
              },
              {
                name: "Elevator",
                icon: "fa-check"
              },
              {
                name: "Air condition",
                icon: "fa-wind"
              },
              {
                name: "Fire alarm",
                icon: "fa-fire"
              },
              {
                name: "Barber",
                icon: "fa-cut"
              }
            ]
          },
          {
            "id": 4,
            "room_type": "double room",
            "photos": [
              "https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
              "https://images.pexels.com/photos/1326946/pexels-photo-1326946.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            ],
            "rooms_left": 5,
            "price": 600,
            "people_number": 2,
            "features": [
              {
                name: "free Wifi",
                icon: "fa-wifi"
              },
              {
                  name: "Restaurant",
                  icon: "fa-utensils"
              },
              {
                  name: "Laundry",
                  icon: "local_laundry_service"
              },
              {
                name: "Market",
                icon: "fa-shopping-cart"
              },
              {
                name: "Elevator",
                icon: "fa-check"
              },
              {
                name: "Air condition",
                icon: "fa-wind"
              },
              {
                name: "Fire alarm",
                icon: "fa-fire"
              },
              {
                name: "Barber",
                icon: "fa-cut"
              } 
            ]
          },
          {
            "id": 2,
            "room_type": "www room",
            "photos": [
              "https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
              "https://images.pexels.com/photos/1326946/pexels-photo-1326946.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            ],
            "rooms_left": 5,
            "price": 1500,
            "people_number": 6,
            "features": [
              {
                name: "free Wifi",
                icon: "fa-wifi"
              },
              {
                  name: "Restaurant",
                  icon: "fa-utensils"
              },
              {
                  name: "Laundry",
                  icon: "local_laundry_service"
              },
              {
                name: "Market",
                icon: "fa-shopping-cart"
              },
              {
                name: "Elevator",
                icon: "fa-check"
              },
              {
                name: "Air condition",
                icon: "fa-wind"
              },
              {
                name: "Fire alarm",
                icon: "fa-fire"
              },
              {
                name: "Barber",
                icon: "fa-cut"
              } 
            ]
          }
        ]
      },
      {
        id: "2",
        name: "DAU Two",
        cover: "https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
        stars: 3.5,
        number_of_reviews: "15",
        geo_longitude: "35.15010",
        geo_latitude: "33.90111",
        address: "EMU Campus, in front of lemar",
        number_of_found_rooms: "15",
        features: [{
          icon: "fa-wifi",
          name: "free wifi"
        },
        {
          icon: "fa-parking",
          name: "free parking"
        },
        {
          icon: "fa-bus",
          name: "free bus"
        },
        {
          icon: "fa-bus",
          name: "free bus"
        }
        ],
        rooms: [
          {
          "id": 15225,
          "room_type": "single room",
          "photos": [
            "https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
            "https://images.pexels.com/photos/1326946/pexels-photo-1326946.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
          ],
          "rooms_left": 5,
          "price": 2000,
          "people_number": 2,
          "features": [
            {
              name: "free Wifi",
              icon: "fa-wifi"
            },
            {
                name: "Restaurant",
                icon: "fa-utensils"
            },
            {
                name: "Laundry",
                icon: "local_laundry_service"
            },
            {
              name: "Market",
              icon: "fa-shopping-cart"
            },
            {
              name: "Elevator",
              icon: "fa-check"
            },
            {
              name: "Air condition",
              icon: "fa-wind"
            },
            {
              name: "Fire alarm",
              icon: "fa-fire"
            },
            {
              name: "Barber",
              icon: "fa-cut"
            } 
          ]
        },
        {
          "id": 15225,
          "room_type": "single room",
          "photos": [
            "https://images.pexels.com/photos/279719/pexels-photo-279719.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
            "https://images.pexels.com/photos/1326946/pexels-photo-1326946.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
          ],
          "rooms_left": 5,
          "price": 2000,
          "people_number": 2,
          "features": [
            {
              name: "free Wifi",
              icon: "fa-wifi"
            },
            {
                name: "Restaurant",
                icon: "fa-utensils"
            },
            {
                name: "Laundry",
                icon: "local_laundry_service"
            },
            {
              name: "Market",
              icon: "fa-shopping-cart"
            },
            {
              name: "Elevator",
              icon: "fa-check"
            },
            {
              name: "Air condition",
              icon: "fa-wind"
            },
            {
              name: "Fire alarm",
              icon: "fa-fire"
            },
            {
              name: "Barber",
              icon: "fa-cut"
            } 
          ]
        }
        ]
      }
      ],
      filters: [],
      filter:{
        "filters": [
            {
              "id": "3",
              "name": "Dorms Activities",
              "checkbox": true,
              "integral": false,
              "options": [
                  {
                      "option_id": 1,
                      "name": "Free sport/Fitness"
                  },
                  {
                      "option_id": 2,
                      "name": "Paid sport/Fitness"
                  },
                  {
                      "option_id": 3,
                      "name": "Other activities"
                  }
              ]
          },
          {
            "id": "3",
            "name": "Dorms Activities",
            "checkbox": true,
            "integral": false,
            "options": [
                {
                    "option_id": 1,
                    "name": "Free sport/Fitness"
                },
                {
                    "option_id": 2,
                    "name": "Paid sport/Fitness"
                },
                {
                    "option_id": 3,
                    "name": "Other activities"
                }
            ]
        },
        {
          "id": "3",
          "name": "Dorms Activities",
          "checkbox": true,
          "integral": false,
          "options": [
              {
                  "option_id": 1,
                  "name": "Free sport/Fitness"
              },
              {
                "option_id": 2,
                "name": "Paid sport/Fitness"
            },
            {
                "option_id": 3,
                "name": "Other activities"
            },
            {
              "option_id": 2,
              "name": "Paid sport/Fitness"
            },
            {
              "option_id": 3,
              "name": "Other activities"
            }
          ]
      },
            {
              "id": 5,
              "name": "Price Range",
              "integral": true,
              "checkbox": false,
              "min_value": 0,
              "max_value": 2000,
              "value": [0, 2000]
            }
        ]
    }
    };
  },
  methods: {
    fetchFilters() {
      this.$backend.$fetchFilters().then(responseDate => {
        this.filters = responseDate
      });
    }
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    drawerControl(){
      return this.$store.state.drawer;
    }
  },
  mounted() {
    this.fetchFilters();
  }
};