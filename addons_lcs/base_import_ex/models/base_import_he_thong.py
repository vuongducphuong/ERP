# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'

class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'   

    def search_menu_by_code(self, code):
        sub_sys_list = self.env['he.thong.sub.system'].search([('SubSystemCode','=',code),('ParentSubSystemCode','!=','SYSOption')])
        mapped_list = []
        for sub_sys in sub_sys_list:
            # Menu
            if not sub_sys.SubSystemSerial.startswith('ROOT/Report'):
                menu = self.env['ir.ui.menu'].search([('name','=',sub_sys.SubSystemName)])
                if len(menu) == 1:
                    mapped_list += [(menu.id,False,sub_sys.SubSystemName)]
                elif len(menu) > 1:
                    for m in menu:
                        parent_sub_sys = self.env['he.thong.sub.system'].search([('SubSystemCode','=',sub_sys.ParentSubSystemCode),('SubSystemName','=',m.parent_id.name),('ParentSubSystemCode','!=','Report'),('ParentSubSystemCode','!=','SYSOption')], limit=1)
                        if parent_sub_sys:
                            mapped_list += [(m.id,False,sub_sys.SubSystemName)]
                            continue
            # Report
            else:
                report = self.env['tien.ich.bao.cao'].search([('TEN_BAO_CAO','=',sub_sys.SubSystemName)])
                if len(report) == 1:
                    mapped_list += [(False,report.id,sub_sys.SubSystemName)]
                elif len(report) > 1:
                    for m in report:
                        parent_sub_sys = self.env['he.thong.sub.system'].search([('SubSystemCode','=',sub_sys.ParentSubSystemCode),('SubSystemName','=',m.parent_id.name),('ParentSubSystemCode','=','Report'),('ParentSubSystemCode','!=','SYSOption')], limit=1)
                        if parent_sub_sys:
                            mapped_list += [(False,m.id,sub_sys.SubSystemName)]

        return mapped_list

    # Update SubSystemCode
    def _import_MSC_SubSystem(self, tag):
        rec_model = 'he.thong.sub.system'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag in ('SubSystemCode','SubSystemName','ParentSubSystemCode','SubSystemSerial'):
                res[child.tag] = child.text
        rec_id = MODULE + '_sub_system_' + res.get('SubSystemCode') + res.get('SubSystemName').replace('.','')
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Vai trò
    def _import_MSC_Role(self, tag):
        rec_model = 'he.thong.vai.tro.va.quyen.han'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RoleID':
                rec_id = child.text
            elif child.tag == 'RoleCode':
                res['MA_VAI_TRO'] =  child.text
            elif child.tag == 'RoleName':
                res['TEN_VAI_TRO'] = child.text
            elif child.tag == 'Description':
                res['MO_TA'] = child.text
            res['THUOC_HE_THONG'] = True

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Danh sách tất cả quyền
    def _import_MSC_Permission(self, tag):
        rec_model = 'he.thong.permission'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'PermissionID':
                rec_id = MODULE + '_he_thong_permission.' + child.text
            res[child.tag] = child.text

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Vai trò gắn với quyền hạn
    def _import_MSC_RolePermissionMaping(self, tag):
        rec_model = 'he.thong.role.permission.mapping'
        res = { }
        rec_id = False
        subSystemCode = False
        for child in tag.getchildren():
            if child.tag == 'ID':
                rec_id = child.text
            elif child.tag == 'SubSystemCode':
                subSystemCode = child.text
            elif child.tag == 'PermissionID':
                if child.text == 'Unpost':
                    child.text = 'UnPost'
                elif child.text in ('use','USE'):
                    child.text = 'Use'
                permission = self.env['he.thong.permission'].search([('PermissionID', '=', child.text)], limit=1)
                if permission:
                    res['permission_id'] = permission.id
            elif child.tag == 'RoleID':
                rid=self.env['ir.model.data'].search([('name','=',child.text),('module','=',MODULE)], limit=1)
                if rid:
                    res['VAI_TRO_ID'] = rid.res_id

        if subSystemCode:
            for menu,report,name in self.search_menu_by_code(subSystemCode):
                if menu:
                    res['menu_id'] = menu
                elif report:
                    res['report_id'] = report
                if res.get('menu_id') or res.get('report_id'):
                    rec_id += name.replace('.','')
                    self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    
    # Menu gắn với quyền hạn
    def _import_MSC_RegisPermisionForSubSystem(self, tag):
        menu = False
        report = False
        permission = False
        subSystemCode = False
        for child in tag.getchildren():
            if child.tag == 'SubSystemCode':
                subSystemCode = child.text
            elif child.tag == 'PermissionID':
                permission = self.env['he.thong.permission'].search([('PermissionID', '=', child.text)], limit=1).id
        for menu,report,_ in self.search_menu_by_code(subSystemCode):
            if menu and permission:
                cr = self.env.cr
                cr.execute("SELECT * FROM msc_regis_permision_for_sub_system WHERE menu_id=%s AND permission_id=%s LIMIT 1", (menu, permission))
                if not cr.rowcount:
                    cr.execute("INSERT INTO msc_regis_permision_for_sub_system (menu_id,permission_id) VALUES (%s,%s)", (menu, permission))
            if report and permission:
                cr = self.env.cr
                cr.execute("SELECT * FROM msc_regis_permision_for_report WHERE report_id=%s AND permission_id=%s LIMIT 1", (report, permission))
                if not cr.rowcount:
                    cr.execute("INSERT INTO msc_regis_permision_for_report (report_id,permission_id) VALUES (%s,%s)", (report, permission))

    # Danh sách mẫu in
    def _import_MSC_ReportTemplate(self, tag):
        rec_model = 'he.thong.mau.in'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'ReportID':
                rec_id = MODULE + '_template_' + child.text
            res[child.tag] = child.text
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)