using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Data
{
	public class StudentRepository : GenericRepository<Student>
	{
		public StudentRepository(DbSet<Student> dbSet) : base(dbSet)
		{
		}
	}
}
