using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Data
{
	public class GenericRepository<T> where T: BaseEntity
	{
		internal readonly DbSet<T> DbSet;

		public GenericRepository(DbSet<T> dbSet)
		{
			DbSet = dbSet;
		}

		public IQueryable<T> GetAll() => DbSet;

		public IQueryable<T> Find(Expression<Func<T, bool>> predicate)
		{
			return DbSet.Where(predicate);
		}

		public T FindById(int id)
		{
			return Find(x => x.Id == id).FirstOrDefault();
		}

		public void Add(IEnumerable<T> entities)
		{
			foreach (var entity in entities)
			{
				DbSet.Add(entity);
			}
		}

		public void Update(IEnumerable<T> entities)
		{
			foreach (var entity in entities)
			{
				DbSet.Update(entity);
			}
		}

		public void Delete(IEnumerable<T> entities)
		{
			foreach (var entity in entities)
			{
				DbSet.Remove(entity);
			}
		}
	}
}