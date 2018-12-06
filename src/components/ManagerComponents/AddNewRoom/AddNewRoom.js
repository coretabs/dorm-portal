export default {
  name: "ManageDorm",
  data: function () {
    return {
      rooms_data :{
	
        room_types :[
          {
            id: 1,
            name: "Single"
          },
          {
            id: 2,
            name: "Double"
          }
        ],
        currencies :[
          {
            id: 1,
            symbol: "$",
            code: "USD"
            
          },
          {
            id: 2,
            symbol: "t",
            code: "TL"
            
          }
        ],
        durations :[
          {
            id: 1,
            name: "summer"
          },
          {
            id: 2,
            name: "spring"
          },
          {
            id: 3,
            name: "fall"
          }
        ],
        room_features :[
          {
            id: 1,
            name: "feature1",
            icon: "fa-wifi"
          },
          {
            id: 1,
            name: "feature2",
            icon: "fa-check"
          }
        ],
        radio_filters :[
          {
            name: "Meals",
            choices: [
              {
                id: 1,
                name: "one meal"
              },
              {
                id: 2,
                name: "two meals"
              }
            ]
          }
        
        ],
        integral_filters :[
          {
            id: 1,
            name: "price"
          },
          {
            id: 2,
            name: "bathrooms"
          }
        ]
      }
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  }
};