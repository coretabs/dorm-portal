using System;
using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Data
{
	public class StudentRepository : GenericRepository<Student>
	{
		public StudentRepository(DbSet<Student> dbSet) : base(dbSet)
		{
		}

		public static explicit operator StudentRepository(GenericRepository<BaseEntity> v)
		{
			throw new NotImplementedException();
		}
	}
}
