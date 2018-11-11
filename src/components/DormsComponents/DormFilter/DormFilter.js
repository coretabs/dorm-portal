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
      drawer: null,
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
        activities: [{
          icon: "fa-swimmer",
          name: "swimming"
        },
        {
          icon: "fa-futbol",
          name: "football"
        },
        {
          icon: "fa-handshake",
          name: "handshake"
        },
        {
          icon: "fa-handshake",
          name: "handshake2"
        }
        ],
        facilities: [{
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
        rooms: [{
          id: "1",
          cover: "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
          price: "1000",
          room_type: "single",
          people_number: "1"
        },
        {
          id: "2",
          cover: "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
          price: "2000",
          room_type: "double",
          people_number: "2"
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
        activities: [{
          icon: "fa-swimmer",
          name: "swimming"
        },
        {
          icon: "fa-futbol",
          name: "football"
        },
        {
          icon: "fa-handshake",
          name: "handshake"
        },
        {
          icon: "fa-handshake",
          name: "handshake2"
        }
        ],
        facilities: [{
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
        rooms: [{
          id: "1",
          cover: "https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
          price: "800",
          room_type: "double",
          people_number: "2"
        },
        {
          id: "2",
          cover: "https://images.pexels.com/photos/189293/pexels-photo-189293.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
          price: "4000",
          room_type: "double",
          people_number: "3"
        }
        ]
      }
      ],
      filters: []
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
    }
  },
  mounted() {
    this.fetchFilters();
  }
};