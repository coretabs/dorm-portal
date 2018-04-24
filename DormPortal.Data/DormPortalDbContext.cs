using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Data
{
    public class DormPortalDbContext : DbContext
    {
		public DormPortalDbContext(DbContextOptions<DormPortalDbContext> options): base(options)
		{
	    }

	    public DbSet<Student> Students { get; set; }
	    public DbSet<Room> Rooms { get; set; }
		public DbSet<Dormitory> Dormitories { get; set; }
    }
}
