using System;
using System.Collections.Generic;
using System.Linq;
using AutoMapper;
using DormPortal.Core.Dtos;
using DormPortal.Core.Models;
using DormPortal.Data;
using DormPortal.Web.Extensions;
using DormPortal.Web.Helpers;
using Microsoft.AspNetCore.JsonPatch;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Web.Controllers
{
	[Route("api/[controller]")]
	public class StudentsController : Controller
	{
		private readonly IUnitOfWork _unitOfWork;

		public StudentsController(IUnitOfWork unitOfWork)
		{
			_unitOfWork = unitOfWork;
		}

		[HttpGet]
		public IActionResult Get()
		{
			var students = _unitOfWork.StudentRepository.GetAll().ToList();
			var result = Mapper.Map<IEnumerable<StudentDto>>(students);

			return Ok(result);
		}

		[HttpGet("{id}", Name = "GET")]
		public IActionResult Get(int id)
		{
			IActionResult result;

			try
			{
				var student = _unitOfWork.StudentRepository.FindById(id);
				result = Ok(Mapper.Map<StudentDto>(student));
			}
			catch (KeyNotFoundException)
			{
				result = NotFound("Could not find the entity with this id");
			}

			return result;
		}

		[HttpPost]
		public IActionResult Post([FromBody] StudentForCreationDto studentDto)
		{
			IActionResult result;

			if (ModelState.IsValid(out result, new []{ studentDto }))
			{
				var student = _unitOfWork.StudentRepository.Add(Mapper.Map<Student>(studentDto));

				if (_unitOfWork.Commit())
				{
					result = CreatedAtRoute("GET", new { id = student.Id }, Mapper.Map<StudentDto>(student));
				}
				else
				{
					throw new Exception("Creating entity failed");
				}
			}

			return result;
		}

		[HttpPut("{id}")]
		public IActionResult Put(int id, [FromBody] StudentForUpdateDto studentDto)
		{
			IActionResult result;

			if (ModelState.IsValid(out result, new[] { studentDto }))
			{
				try
				{
					var student = _unitOfWork.StudentRepository.FindById(id);
					Mapper.Map(studentDto, student);

					_unitOfWork.StudentRepository.Update(student);
					_unitOfWork.Commit();
					result = Ok(student);
				}
				catch (KeyNotFoundException)
				{
					result = NotFound("Could not find the entity with this id");
				}
			}

			return result;
		}

		[HttpPatch("{id}")]
		public IActionResult Patch(int id, [FromBody] JsonPatchDocument<StudentForUpdateDto> studentPatch)
		{
			IActionResult result;

			if (ModelState.IsValid(out result, new[] { studentPatch }))
			{
				try
				{
					var student = _unitOfWork.StudentRepository.FindById(id);
					var studentDto = Mapper.Map<StudentForUpdateDto>(student);
					studentPatch.ApplyTo(studentDto, ModelState);
					TryValidateModel(studentDto);

					if (ModelState.IsValid(out result))
					{
						Mapper.Map(studentDto, student);

						_unitOfWork.StudentRepository.Update(student);
						_unitOfWork.Commit();
						result = Ok(student);
					}
					
				}
				catch (KeyNotFoundException)
				{
					result = NotFound("Could not find the entity with this id");
				}
			}

			return result;
		}

		[HttpDelete("{id}")]
		public IActionResult Delete(int id)
		{
			IActionResult result;

			try
			{
				_unitOfWork.StudentRepository.Delete(id);
				_unitOfWork.Commit();
				result = NoContent();
			}
			catch (DbUpdateConcurrencyException)
			{
				result = NotFound("Could not find the entity with this id");
			}

			return result;
		}
	}
}
