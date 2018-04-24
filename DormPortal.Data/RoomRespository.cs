using System.Collections.Generic;
using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Data
{
    public class RoomRespository : GenericRepository<Room>
    {
	    public RoomRespository(DbSet<Room> dbSet) : base(dbSet)
	    {
	    }

	    public IEnumerable<Room> GetAvailableRooms()
	    {
		    return Find(room => room.IsReserved == false);
	    }

	    public bool ReserveRoom(int id)
	    {
		    var currentRoom = FindById(id);

		    currentRoom.IsReserved = true;

		    return true;
	    }
    }
}
