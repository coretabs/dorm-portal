using System.Collections.Generic;

namespace DormPortal.Core.Models
{
    public class Dormitory
    {
	    public int Id { get; set; }
		public string Name { get; set; }
	    public ICollection<Room> Rooms { get; set; }
    }
}
