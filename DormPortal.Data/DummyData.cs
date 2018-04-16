using System.Collections.Generic;
using DormPortal.Core.Models;

namespace DormPortal.Data
{
	public class DummyData
	{
		public static List<Student> Students => new List<Student>()
		{
			new Student{Name = "Yaser", PassportNumber = "484245aa"},
			new Student{Name = "Mohammed", PassportNumber = "7d5g4sd4"},
			new Student{Name = "Nonsu", PassportNumber = "8494sega"},
			new Student{Name = "Yagmur", PassportNumber = "59f54hr"},
		};

		public static List<Room> Rooms => new List<Room>()
		{
			new Room(){IsReserved = false, Dormitory = Dormitories[0]},
			new Room(){IsReserved = true, Dormitory = Dormitories[0]},
			new Room(){IsReserved = false, Dormitory = Dormitories[0]},

			new Room(){IsReserved = false, Dormitory = Dormitories[1]},
			new Room(){IsReserved = true, Dormitory = Dormitories[1]},
			new Room(){IsReserved = true, Dormitory = Dormitories[1]},
		};


		public static List<Dormitory> Dormitories => new List<Dormitory>()
		{
			new Dormitory {Name = "Longson",},
			new Dormitory {Name = "HomeDorm",},
		};
	}
}
