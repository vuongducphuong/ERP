# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields

class TIEN_ICH_THUC_HIEN_NGHIA_VU_DOI_VOI_NHA_NUOC_CHI_TIET_MAC_DINH(models.Model):
    _name = 'tien.ich.thuc.hien.nghia.vu.doi.voi.nha.nuoc.mac.dinh'
    _description = ''
    _inherit = ['mail.thread']
    MA_CHI_TIEU = fields.Char(string='Mã chỉ tiêu', help='Mã chỉ tiêu')
    TEN_CHI_TIEU = fields.Char(string='Tên chỉ tiêu', help='Tên chỉ tiêu')
    TEN_TIENG_ANH = fields.Char(string='Tên tiếng anh', help='Tên tiếng anh')
    LOAI_CHI_TIEU = fields.Selection([('0', 'Chi tiết'), ('1', 'Tổng hợp'), ('2', 'Tiêu đề'),('3', 'Chú thích'), ], string='Loại chỉ tiêu', help='Loại chỉ tiêu', default='0' , required=True)
    SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG = fields.Char(string='Số còn phải nộp kỳ trước chuyển sang', help='Số còn phải nộp kỳ trước chuyển sang')
    SO_PHAI_NOP_TRONG_KY = fields.Char(string='Số phải nộp trong kỳ', help='Số phải nộp trong kỳ')
    SO_DA_NOP_TRONG_KY = fields.Char(string='Số đã nộp trong kỳ', help='Số đã nộp trong kỳ')
    KHONG_IN = fields.Boolean(string='Không in', help='Không in')
    IN_DAM = fields.Boolean(string='In đậm', help='In đậm')
    IN_NGHIENG = fields.Boolean(string='In nghiêng', help='In nghiêng')
    THONG_TU  = fields.Char(string='Thông tư' , help = 'Thông tư')
    XAY_DUNG_CONG_THUC  = fields.Char(string='Thông tư' , help = 'Thông tư')
    name = fields.Char(string='Name', help='Name', oldname='NAME')

    SO_THU_TU = fields.Integer(string='Số thứ tự các dòng chi tiết', help='Số thứ tự các dòng chi tiết')

    TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS = fields.One2many('tien.ich.ththnvdvnnpntk.lct.chi.tiet.mac.dinh', 'CHI_TIET_ID', string='Tình hình THNVDVNN PNTK loại chỉ tiêu chi tiết')
    TIEN_ICH_TINH_HINH_THNVDVNN_PNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS = fields.One2many('tien.ich.ththnvdvnnpntk.lct.tong.hop.mac.dinh', 'CHI_TIET_ID', string='Tình hình THNVDVNN PNTK loại chỉ tiêu tổng hợp')
    TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_CHI_TIET_MD_IDS = fields.One2many('tien.ich.ththnvdvnndntk.lct.chi.tiet.mac.dinh', 'CHI_TIET_ID', string='Tình hình THNVDVNN DNTK loại chỉ tiêu chi tiết')
    TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_TONG_HOP_MD_IDS = fields.One2many('tien.ich.ththnvdvnnpnkt.lct.tong.hop.mac.dinh', 'CHI_TIET_ID', string='Tình hình THNVDVNN PNKT loại chỉ tiêu tổng hợp')
    TIEN_ICH_TINH_HINH_THNVDVNN_PNKT_LOAI_CHI_TIEU_CHI_TIET_MD_IDS = fields.One2many('tien.ich.ththnvdvnnpnkt.lct.chi.tiet.mac.dinh', 'CHI_TIET_ID', string='Tình hình THNVDVNN PNKT loại chỉ tiêu chi tiết ')
    TIEN_ICH_TINH_HINH_THNVDVNN_DNTK_LOAI_CHI_TIEU_TONG_HOP_MD_IDS = fields.One2many('tien.ich.ththnvdvnndntk.lct.tong.hop.mac.dinh', 'CHI_TIET_ID', string='Tình hình THNVDVNN DNTK loại chỉ tiêu tổng hợp')