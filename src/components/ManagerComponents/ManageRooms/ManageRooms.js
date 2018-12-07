
export default {
  name: "ManageRooms",
  data: function () {
    return {
      showQuotaUpdatedialog: false,
      showRoomDetailsdialog: false,
      reservedRoomsNumber: null,
      totalRoomsNumber: null,
      allowedQuotaNumber: null,
      availableRoomsNumber: null,
      quotaRoomID: null,
      roomDetails: {},
      items: [
        { title: 'Edit' },
        { title: 'Delete' }
      ],
      room_cards:[
        {
          id:1,
          room_type: "Single room",
          total_rooms: 100,
          reserved_rooms: 50,
          allowed_quota: 10,
          price: 1500,
          people: 2,
          currency: "USD",
          features1: [
            {
              name: "free wifi",
              icon: "fa-wifi"
            },
            {
              name: "Parking",
              icon: "fa-check"
            }
          ],
          features2:[
            {
              name: "meals",
              choice: "One meal"
            },
            {
              name: "another feature",
              choice: "24/7 reception"
            }
          ],
          photos:[
            {
              id: 1,
              url: "https://images.pexels.com/photos/1082326/pexels-photo-1082326.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            },
            {
              id: 1,
              url: "https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            }
          ]
        },
        {
          id:2,
          room_type: "Single room",
          total_rooms: 20,
          reserved_rooms: 3,
          allowed_quota: 15,
          price: 1500,
          people: 2,
          currency: "USD",
          features1: [
            {
              name: "free wifi",
              icon: "fa-wifi"
            },
            {
              name: "Parking",
              icon: "fa-check"
            }
          ],
          features2:[
            {
              name: "meals",
              choice: "One meal"
            },
            {
              name: "another feature",
              choice: "24/7 reception"
            }
          ],
          photos:[
            {
              id: 1,
              url: "https://images.pexels.com/photos/1082326/pexels-photo-1082326.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            },
            {
              id: 1,
              url: "https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            }
          ]
        },
        {
          id:3,
          room_type: "Double room",
          total_rooms: 60,
          reserved_rooms: 59,
          allowed_quota: 1,
          price: 1500,
          currency: "USD",
          people: 2,
          features1: [
            {
              name: "free wifi",
              icon: "fa-wifi"
            },
            {
              name: "Parking",
              icon: "fa-check"
            }
          ],
          features2:[
            {
              name: "meals",
              choice: "One meal"
            },
            {
              name: "another feature",
              choice: "24/7 reception"
            }
          ],
          photos:[
            {
              id: 1,
              url: "https://images.pexels.com/photos/1082326/pexels-photo-1082326.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            },
            {
              id: 1,
              url: "https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            }
          ]
        },
        {
          id:4,
          room_type: "Delux room",
          total_rooms: 60,
          reserved_rooms: 45,
          allowed_quota: 5,
          price: 1500,
          people: 2,
          currency: "USD",
          features1: [
            {
              name: "free wifi",
              icon: "fa-wifi"
            },
            {
              name: "Parking",
              icon: "fa-check"
            }
          ],
          features2:[
            {
              name: "meals",
              choice: "One meal"
            },
            {
              name: "another feature",
              choice: "24/7 reception"
            }
          ],
          photos:[
            {
              id: 1,
              url: "https://images.pexels.com/photos/1082326/pexels-photo-1082326.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            },
            {
              id: 1,
              url: "https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            }
          ]
        },
        {
          id:4,
          room_type: "Delux room",
          total_rooms: 20,
          reserved_rooms: 20,
          allowed_quota: 0,
          price: 1500,
          people: 2,
          currency: "USD",
          features1: [
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
            }
          ],
          features2:[
            {
              name: "Campus",
              choice: "Northern campus"
            },{
              name: "Meals",
              choice: "Breakfast & Dinner"
            },{
              name: "Dorm Activities",
              choice: "Free sport/fitness"
            }
          ],
          photos:[
            {
              id: 1,
              url: "https://images.pexels.com/photos/1082326/pexels-photo-1082326.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            },
            {
              id: 1,
              url: "https://images.pexels.com/photos/97904/pexels-photo-97904.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            }
          ]
        }
      ]
    };
  },
  computed: {
    lang() {
      return this.USDstore.getters.lang;
    }    
  },
  methods:{
    loadComponent(componentName){
      this.USDroot.USDemit('currentTabComponent', componentName)
    },
    showRoomDetails(room){
      this.roomDetails = room;
      this.showRoomDetailsdialog = true;
    },
    showQuotaUpdate(reservedRooms, totalRooms, allowedQuota, roomID){
      this.reservedRoomsNumber = reservedRooms;
      this.totalRoomsNumber = totalRooms;
      this.allowedQuotaNumber = allowedQuota;
      this.quotaRoomID = roomID;
      this.showQuotaUpdatedialog = true;
    },
    progressValue(reserved_rooms,total_rooms){
      return reserved_rooms / total_rooms * 100;
    },
    availableRooms(reserved_rooms, total_rooms){
      this.availableRoomsNumber = total_rooms - reserved_rooms;
      return this.availableRoomsNumber;
    },
    progressColor(reservedRooms, totalRooms){

      var avg = reservedRooms/totalRooms*100;

      return (avg > 90) ? "#cf5151" : (avg > 50) ? "#ec7811" : "#39c463";
      
    },
    quotaTextColor(quota){
      return quota == 0 ? "red--text" : "black--text";
    }
  }
};