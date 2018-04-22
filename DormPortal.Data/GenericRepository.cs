using System;
using System.Linq;
using System.Linq.Expressions;
using DormPortal.Core.Models;

namespace DormPortal.Data
{
	public class GenericRepository<T> where T: IEntity
	{
		internal readonly IQueryable<T> DbSet;

		public GenericRepository(IQueryable<T> dbSet)
		{
			DbSet = dbSet;
		}

		public IQueryable<T> GetAll => DbSet;

		public IQueryable<T> Find(Expression<Func<T, bool>> predicate)
		{
			return DbSet.Where(predicate);
		}

		public T FindById(int id)
		{
			return Find(x => x.Id == id).FirstOrDefault();
		}
	}
}