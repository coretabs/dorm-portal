import FileUpload from 'vue-upload-component/src'

export default {
  name: "ManageDorm",
  components: {
    'file-upload': FileUpload
  },
  data: function () {
    return {
      selectedFeatures:[],
      files: [],
      isUpdating: false,
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
            name: "feature1"
          },
          {
            id: 2,
            name: "feature2"
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
          },
          {
            name: "Parking",
            choices: [
              {
                id: 1,
                name: "Yes"
              },
              {
                id: 2,
                name: "no"
              }
            ]
          }
        
        ],
        integral_filters :[
          {
            id: 1,
            name: "Number of Condition"
          },
          {
            id: 2,
            name: "Number Bathrooms"
          }
        ]
      }
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods: {
    remove (item) {
      const index = this.selectedFeatures.indexOf(item.id)
      if (index >= 0) this.selectedFeatures.splice(index, 1)
    }
  },
  watch: {
    isUpdating (val) {
      if (val) {
        setTimeout(() => (this.isUpdating = false), 3000)
      }
    }
  }
};