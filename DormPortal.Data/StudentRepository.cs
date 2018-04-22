using System.Linq;
using DormPortal.Core.Models;

namespace DormPortal.Data
{
	public class StudentRepository : GenericRepository<Student>
	{
		public StudentRepository(IQueryable<Student> dbSet) : base(dbSet)
		{
		}
	}
}
