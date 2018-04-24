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

		public IActionResult Get(int id)
		{
			return Ok(_unitOfWork.StudentRepository.FindById(id));
		}

		public IActionResult Post(Student student)
		{
			//var result = _unitOfWork.Add<Student>(student);
			var result = student;
			_unitOfWork.Commit();

			return Ok(result);
		}

		public IActionResult Put(int id, Student student)
		{
			var studentToUpdate = _unitOfWork.StudentRepository.FindById(id);
			//var result = _unitOfWork.Update(student);
			_unitOfWork.Commit();

			//return Ok(result);
			return Ok("");
		}

		//  public IActionResult Delete(Student student)
		//  {
		//var result = _unitOfWork.Delete(student);
		//   _unitOfWork.Commit();

		//   return Ok(result);
		//  }
	}
}
