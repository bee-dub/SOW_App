import tkinter as tk
from tkinter import ttk, messagebox
from sow_db import SOW_Database

class GUI:
    def __init__(self, master):
        self.master = master

        # configure row & column
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=100)

        # frames
        self.frame0 = tk.Frame(self.master)
        self.frame0.grid(row=0, column=0, sticky='we', padx=10, pady=(20,10))
        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(row=1, column=0, sticky='we', padx=10, pady=10)
        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=2, column=0, sticky='nswe')
        self.frame3 = tk.Frame(self.master)
        self.frame3.grid(row=3, column=0, sticky='we')

        # navigation & edit
        self.add_nav_edit()

        # populate master window
        self.add_buttons_labels_entries()

        # populate treeview
        db = SOW_Database()
        rows = db.sow_records()
        self.add_treeview()
        self.populate_treeview(db, rows)

        # populate entry box for edit
        self.populate_data_for_edit(1)

    def add_nav_edit(self):
        frm = self.frame0
        padx_amt = 1
        btn_size = 3

        # nav
        grp_nav = ttk.LabelFrame(frm, text='Navigate/New/Update')
        grp_nav.pack(side=tk.LEFT)
        btn_first = ttk.Button(grp_nav, text='<|', width=btn_size)
        btn_first.grid(row=1, column=0, sticky=tk.W)
        btn_first = ttk.Button(grp_nav, text='<', width=btn_size)
        btn_first.grid(row=1, column=0, sticky=tk.W, padx=(28, 0))
        btn_first = ttk.Button(grp_nav, text='>', width=btn_size)
        btn_first.grid(row=1, column=0, sticky=tk.W, padx=(56, 0))
        btn_first = ttk.Button(grp_nav, text='|>', width=btn_size)
        btn_first.grid(row=1, column=0, sticky=tk.W, padx=(84, 0))
        btn_save = ttk.Button(grp_nav, text='New', width=btn_size + 2)
        btn_save.grid(row=1, column=0, sticky=tk.W, padx=(118, 0))
        btn_save = ttk.Button(grp_nav, text='Save', width=btn_size + 2)
        btn_save.grid(row=1, column=0, sticky=tk.W, padx=(158, 0))

        # group box - search
        grp_box = ttk.LabelFrame(frm, text='Search')
        grp_box.pack(side=tk.LEFT, padx=20)
        # sow name
        lbl_sow_name = ttk.Label(grp_box, text='SOW Name')
        lbl_sow_name.pack(side=tk.LEFT)
        self.ent_sow_name_search = ttk.Entry(grp_box)
        self.ent_sow_name_search.pack(side=tk.LEFT, padx=padx_amt)
        # sow owner wipro
        lbl_sow_owner_wipro = ttk.Label(grp_box, text='SOW Owner (Wipro)')
        lbl_sow_owner_wipro.pack(side=tk.LEFT)
        self.ent_sow_owner_wipro_search = ttk.Entry(grp_box)
        self.ent_sow_owner_wipro_search.pack(side=tk.LEFT, padx=padx_amt)
        # sow owner chc
        lbl_sow_owner_chc = ttk.Label(grp_box, text='SOW Owner (CHC)')
        lbl_sow_owner_chc.pack(side=tk.LEFT)
        self.ent_sow_owner_chc_search = ttk.Entry(grp_box)
        self.ent_sow_owner_chc_search.pack(side=tk.LEFT, padx=padx_amt)
        # search button
        btn_search = ttk.Button(grp_box, text='Search', width=6, command=self.search_command)
        btn_search.pack(side=tk.LEFT, padx=padx_amt)

    def search_command(self):
        self.treeview.delete(*self.treeview.get_children())  # clear tree
        db = SOW_Database()
        rows = db.search_records(self.ent_sow_name_search.get(), self.ent_sow_owner_wipro_search.get(), self.ent_sow_owner_chc_search.get())
        self.populate_treeview(db, rows, False)
        del db

        self.populate_data_for_edit(1)

    def select_all_command(self):
        pass

    def add_buttons_labels_entries(self):
        frm = self.frame1
        left_align = 'w'
        both_align = 'we'
        pad_y_amt = 2
        pad_x_amt = 5

        # s. no
        lbl_sno_name = ttk.Label(frm, text='S. No')
        lbl_sno_name.grid(row=0, column=0, sticky=left_align, pady=pad_y_amt)
        self.lbl_sno_value = ttk.Label(frm, text='', relief=tk.SUNKEN, anchor=tk.CENTER)
        self.lbl_sno_value.grid(row=0, column=1, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # bu code
        lbl_bu_code = ttk.Label(frm, text='BU Code')
        lbl_bu_code.grid(row=1, column=0, sticky=left_align, pady=pad_y_amt)
        self.ent_bu_code = ttk.Entry(frm)
        self.ent_bu_code.grid(row=1, column=1, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # sow id
        lbl_sow_id = ttk.Label(frm, text='SOW ID')
        lbl_sow_id.grid(row=1, column=2, sticky=left_align)
        self.ent_sow_id = ttk.Entry(frm)
        self.ent_sow_id.grid(row=1, column=3, sticky=both_align, padx=pad_x_amt)
        # chc bu
        lbl_chc_bu = ttk.Label(frm, text='CHC BU')
        lbl_chc_bu.grid(row=1, column=4, sticky=left_align)
        self.ent_chc_bu = ttk.Entry(frm)
        self.ent_chc_bu.grid(row=1, column=5, sticky=both_align, padx=pad_x_amt)
        # type
        lbl_type = ttk.Label(frm, text='Type')
        lbl_type.grid(row=2, column=0, sticky=left_align)
        self.ent_type = ttk.Entry(frm)
        self.ent_type.grid(row=2, column=1, sticky=both_align, padx=pad_x_amt)
        # chc bu
        lbl_tower = ttk.Label(frm, text='Tower')
        lbl_tower.grid(row=2, column=2, sticky=left_align)
        self.ent_tower = ttk.Entry(frm)
        self.ent_tower.grid(row=2, column=3, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # sow name
        lbl_sow_name = ttk.Label(frm, text='SOW Name')
        lbl_sow_name.grid(row=3, column=0, sticky=left_align, pady=pad_y_amt)
        self.ent_sow_name = ttk.Entry(frm)
        self.ent_sow_name.grid(row=3, column=1, columnspan=3, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # engagement model
        lbl_eng_mdl = ttk.Label(frm, text='Engagement Model')
        lbl_eng_mdl.grid(row=3, column=4, sticky=left_align)
        self.ent_eng_mdl = ttk.Entry(frm)
        self.ent_eng_mdl.grid(row=3, column=5, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # sow owner wipro
        lbl_sow_owner_wipro = ttk.Label(frm, text='SOW Owner (Wipro)')
        lbl_sow_owner_wipro.grid(row=4, column=0, sticky=left_align)
        self.ent_sow_owner_wipro = ttk.Entry(frm)
        self.ent_sow_owner_wipro.grid(row=4, column=1, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # sow owner chc
        lbl_sow_owner_chc = ttk.Label(frm, text='SOW Owner (CHC)')
        lbl_sow_owner_chc.grid(row=4, column=4, sticky=left_align)
        self.ent_sow_owner_chc = ttk.Entry(frm)
        self.ent_sow_owner_chc.grid(row=4, column=5, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # offshore
        lbl_offshore = ttk.Label(frm, text='Offshore')
        lbl_offshore.grid(row=5, column=0, sticky=left_align, pady=pad_y_amt)
        self.ent_offshore = ttk.Entry(frm)
        self.ent_offshore.grid(row=5, column=1, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # Onsite
        lbl_onsite = ttk.Label(frm, text='Onsite')
        lbl_onsite.grid(row=5, column=2, sticky=left_align)
        self.ent_onsite = ttk.Entry(frm)
        self.ent_onsite.grid(row=5, column=3, sticky=both_align, padx=pad_x_amt)
        # total fte
        lbl_ttl_fte = ttk.Label(frm, text='Total FTE')
        lbl_ttl_fte.grid(row=5, column=4, sticky=left_align)
        self.ent_ttl_fte = ttk.Entry(frm)
        self.ent_ttl_fte.grid(row=5, column=5, sticky=both_align, padx=pad_x_amt)
        # sow value
        lbl_sow_value = ttk.Label(frm, text='SOW Value')
        lbl_sow_value.grid(row=5, column=6, sticky=left_align)
        self.ent_sow_value = ttk.Entry(frm)
        self.ent_sow_value.grid(row=5, column=7, sticky=both_align, padx=pad_x_amt)
        # start date
        lbl_start_date = ttk.Label(frm, text='Start Date')
        lbl_start_date.grid(row=6, column=0, sticky=left_align, pady=pad_y_amt)
        self.ent_start_date = ttk.Entry(frm)
        self.ent_start_date.grid(row=6, column=1, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # end date
        lbl_end_date = ttk.Label(frm, text='End Date')
        lbl_end_date.grid(row=6, column=2, sticky=left_align)
        self.ent_end_date = ttk.Entry(frm)
        self.ent_end_date.grid(row=6, column=3, sticky=both_align, padx=pad_x_amt)
        # Status
        lbl_status = ttk.Label(frm, text='Status')
        lbl_status.grid(row=6, column=4, sticky=left_align)
        self.ent_status = ttk.Entry(frm)
        self.ent_status.grid(row=6, column=5, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # remarks
        lbl_remarks = ttk.Label(frm, text='Remarks')
        lbl_remarks.grid(row=7, column=0, sticky=left_align, pady=pad_y_amt)
        self.txt_remarks = tk.Text(frm, height=4, width=1, font=('Helvetica', 9))
        self.txt_remarks.grid(row=7, column=1, columnspan=7, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)

    def add_treeview(self):
        # add treeview
        self.treeview = ttk.Treeview(self.frame2)
        self.treeview.pack(expand=True, fill=tk.BOTH)

        # hsb
        hsb = ttk.Scrollbar(self.frame3, orient=tk.HORIZONTAL, command=self.treeview.xview)
        hsb.pack(fill=tk.X)
        self.treeview.configure(xscrollcommand=hsb.set)

        # vsb
        vsb = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.treeview.yview)
        vsb.grid(row=2, column=1, sticky=tk.N + tk.S)
        self.treeview.configure(yscrollcommand=vsb.set)

    def populate_treeview(self, db, record_list, add_columns_n_headers=True):
        lst = record_list

        if add_columns_n_headers:
            # add columns
            hdr_list = []
            for idx, row in enumerate(db.cursor.description):
                hdr_list.append(row[0])
            self.treeview.config(columns=tuple(hdr_list))

            # add column names
            for i in hdr_list:
                self.treeview.heading(i, text=i)

        # add data to columns
        for idx, row in enumerate(lst):
            # add "iid" to get value from row and item within row
            self.treeview.insert('', 'end', iid=idx+1, text=str(idx+1), values=tuple(row))

            self.treeview.column("#0", width=50)
            self.treeview.column("#1", width=75)

    def navigate_records(self, event):
        tree = self.treeview
        try:
            btn_text = event.widget.cget('text')
            cur_row = tree.selection()[0]
            last_row = len(tree.get_children())
            if btn_text == '>':
                if cur_row == str(last_row):
                    itm = last_row
                    tree.selection_set(itm)
                else:
                    itm = tree.next(cur_row)
                    tree.selection_set(itm)
            elif btn_text == '<':
                if cur_row == '1':
                    itm = 1
                    tree.selection_set(itm)
                else:
                    itm = tree.prev(cur_row)
                    tree.selection_set(itm)
            elif btn_text == '>|':
                tree.selection_set(last_row)
                tree.yview_moveto(last_row)
                itm = last_row
            elif btn_text == '|<':
                itm = 1
                tree.selection_set(itm)
                tree.yview_moveto(0)
            self.populate_data_for_edit(itm)
        except IndexError as ie:
            messagebox.showerror('Error', ie)
        except Exception as e:
            messagebox.showerror('Error', e)

    def populate_data_for_edit(self, iid_id):
        self.lbl_sno_value.config(text=self.treeview.item(iid_id)['values'][0])
        self.ent_bu_code.insert(tk.END, self.treeview.item(iid_id)['values'][1])
        self.ent_sow_id.insert(tk.END, self.treeview.item(iid_id)['values'][2])
        self.ent_chc_bu.insert(tk.END, self.treeview.item(iid_id)['values'][3])
        self.ent_type.insert(tk.END, self.treeview.item(iid_id)['values'][4])
        self.ent_tower.insert(tk.END, self.treeview.item(iid_id)['values'][5])
        self.ent_sow_name.insert(tk.END, self.treeview.item(iid_id)['values'][6])
        self.ent_eng_mdl.insert(tk.END, self.treeview.item(iid_id)['values'][7])
        self.ent_sow_owner_wipro.insert(tk.END, self.treeview.item(iid_id)['values'][8])

        self.ent_sow_owner_chc.insert(tk.END, self.treeview.item(iid_id)['values'][9])
        self.ent_offshore.insert(tk.END, self.treeview.item(iid_id)['values'][10])
        self.ent_onsite.insert(tk.END, self.treeview.item(iid_id)['values'][11])
        self.ent_ttl_fte.insert(tk.END, self.treeview.item(iid_id)['values'][12])
        self.ent_sow_value.insert(tk.END, self.treeview.item(iid_id)['values'][13])
        self.ent_start_date.insert(tk.END, self.treeview.item(iid_id)['values'][14])
        self.ent_end_date.insert(tk.END, self.treeview.item(iid_id)['values'][15])
        self.ent_status.insert(tk.END, self.treeview.item(iid_id)['values'][16])
        self.txt_remarks.insert(tk.END, self.treeview.item(iid_id)['values'][17])

        self.treeview.selection_add(iid_id) # select & highlight row in treeview


def main():
    root = tk.Tk()
    root.title('SOW')
    root.geometry('1000x600')
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()