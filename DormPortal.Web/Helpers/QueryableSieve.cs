using System;
using System.Collections.Generic;
using System.Dynamic;
using System.Linq;
using System.Reflection;
using AutoMapper;
using AutoMapper.QueryableExtensions;
using DormPortal.Core.Dtos;
using DormPortal.Core.Helpers;
using Sieve.Services;

namespace DormPortal.Web.Helpers
{
	public static class QueryableSieve
	{
		public static IEnumerable<ExpandoObject> Apply<T>(this ISieveProcessor sieveProcessor, 
			SieveModel sieveModel, IQueryable<T> data)
		{
			IEnumerable<ExpandoObject> result;

			if (sieveModel == null)
			{
				result = Mapper.Map<IEnumerable<StudentDto>>(data.ToList()) as IEnumerable<ExpandoObject>;
			}
			else
			{
				result = sieveProcessor.Apply(sieveModel, data).ProjectTo<StudentDto>()
							.ShapeData(sieveModel.Fields).ToList();
			}

			return result;
		}

		public static IEnumerable<ExpandoObject> ShapeData<T>(
			this IQueryable<T> source,
			string fields)
		{
			if (source == null)
			{
				throw new ArgumentNullException(nameof(source));
			}

			var expandoObjectList = new List<ExpandoObject>();

			var propertyInfoList = new List<PropertyInfo>();

			if (string.IsNullOrWhiteSpace(fields))
			{
				var propertyInfos = typeof(T)
					.GetProperties(BindingFlags.Public | BindingFlags.Instance);

				propertyInfoList.AddRange(propertyInfos);
			}
			else
			{
				var fieldsAfterSplit = fields.Split(',');

				foreach (var field in fieldsAfterSplit)
				{
					var propertyName = field.Trim();

					var propertyInfo = typeof(T)
						.GetProperty(propertyName, BindingFlags.IgnoreCase | BindingFlags.Public | BindingFlags.Instance);

					if (propertyInfo == null)
					{
						throw new Exception($"Property {propertyName} wasn't found on {typeof(T)}");
					}

					propertyInfoList.Add(propertyInfo);
				}
			}

			foreach (T sourceObject in source)
			{
				var dataShapedObject = new ExpandoObject();

				foreach (var propertyInfo in propertyInfoList)
				{
					var propertyValue = propertyInfo.GetValue(sourceObject);

					((IDictionary<string, object>)dataShapedObject).Add(propertyInfo.Name, propertyValue);
				}

				expandoObjectList.Add(dataShapedObject);
			}

			return expandoObjectList;
		}
	}
}
