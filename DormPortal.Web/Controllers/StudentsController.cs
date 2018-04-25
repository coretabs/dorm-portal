using System;
using System.Collections.Generic;
using System.Linq;
using AutoMapper;
using DormPortal.Core.Dtos;
using DormPortal.Core.Models;
using DormPortal.Data;
using Microsoft.AspNetCore.Mvc;

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

			if (studentDto == null)
			{
				result = BadRequest();
			}

			var student = _unitOfWork.StudentRepository.Add(Mapper.Map<Student>(studentDto));

			if (_unitOfWork.Commit())
			{
				result = CreatedAtRoute("GET", new {id = student.Id}, Mapper.Map<StudentDto>(student));
			}
			else
			{
				throw new Exception("Creating entity failed");
			}

			return result;
		}

		public IActionResult Put(int id, Student student)
		{
			var studentToUpdate = _unitOfWork.StudentRepository.FindById(id);
			//var result = _unitOfWork.Update(student);
			_unitOfWork.Commit();

			//return Ok(result);
			return Ok("");
		}

		[HttpDelete("{id}")]
		public IActionResult Delete(int id)
		{
			_unitOfWork.StudentRepository.Delete(id);
			_unitOfWork.Commit();

			return NoContent();
		}
	}
}
