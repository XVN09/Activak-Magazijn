//
//  TableViewController.swift
//  ActivakMagazijn1.0
//
//  Created by Xander Van nuffel on 14/04/2023.
//

import Foundation
import FirebaseStorage
import FirebaseDatabase
import UIKit
import FirebaseAuth

class TableViewController :  UIViewController, UITableViewDelegate, UITableViewDataSource{
    
    
    @IBOutlet weak var tableView : UITableView!
    var dataArray : [MyData] = []
    let reuseIdentifier = "DataCell"
    
    
    override func viewDidLoad() {
        tableView.delegate = self
        tableView.dataSource = self
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return dataArray.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: reuseIdentifier, for: indexPath) as? DataCell else {
            return UITableViewCell()
        }
        cell.setValues(data: dataArray[indexPath.row])
        
        return cell
    }
    


    //function to determine where to send to after pressing account button
    @IBAction func buttonAction(_ sender: Any) {
    
        if Auth.auth().currentUser?.uid != nil
            {
            //User is logged in
            self.performSegue(withIdentifier: "LoggedInSegue", sender: nil)
            
            } else
            {
                //user is not logged in
                self.performSegue(withIdentifier: "AccountStartScreenSegue", sender: nil)
            }
    }
}
